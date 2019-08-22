## Framework for Sentence Mover's Distance

import sys, nltk

import numpy as np
import spacy
import math
from wmd import WMD
from nltk.corpus import stopwords
from collections import Counter
from allennlp.commands.elmo import ElmoEmbedder

stop_words = set(stopwords.words('english'))
WORD_REP = "glove"
METRIC = "s+wms"

def tokenize_texts(inLines):
	# input: raw input text
	# output: a list of token IDs, where a id_doc=[[ref],[hyp]],
	#           ref/hyp=[sent1, sent2,...], and a sent=[wordID1, wordID2 ... ]

	id_docs = []
	# TODO: rewrite this
	text_docs = []

	for doc in inLines:
		id_doc = []
		# TODO: rewrite this
		text_doc = []

		for i in range(2):  # iterate over ref and hyp
			text = doc[i].strip()
			sent_list = [sent for sent in nltk.sent_tokenize(text)]
			if WORD_REP == "glove":
				IDs = [[nlp.vocab.strings[t.text.lower()] for t in nlp(sent) if t.text.isalpha() and t.text.lower() not in stop_words] for sent in sent_list]
			if WORD_REP == "elmo":
				# no word IDs, just use spacy ids, but without lower/stop words
				# IDs = [[nlp.vocab.strings[t.text] for t in nlp(sent)] for sent in sent_list]
				IDs = [[nlp.vocab.strings[t.text] for t in nlp(sent)] for sent in sent_list]
			id_list = [x for x in IDs if x != []]  # get rid of empty sents
			# TODO: rewrite this
			text_list = [[token.text for token in nlp(x)] for x in sent_list if x != []]

			id_doc.append(id_list)
			# TODO: rewrite this
			text_doc.append(text_list)
		id_docs.append(id_doc)
		# TODO: rewrite this
		text_docs.append(text_doc)
	#TODO: rewrite this
	return id_docs, text_docs


def get_embeddings(id_doc, text_doc):

	# input: a ref/hyp pair, with each piece is a list of sentences and each sentence is a list of token IDs
	# output: IDs (the orig doc but updating IDs as needed) and rep_map (a dict mapping word ids to embeddings).
	#           if sent emb, add list of sent emb to end of ref and hyp

	rep_map = {}

	# if adding new IDs, make sure they don't overlap with existing IDs
	# to get max, flatten the list of IDs
	new_id = max(sum(sum(id_doc, []), [])) + 1

	sent_ids = [[], []]  # keep track of sentence IDs for rep and hyp. won't use this for wms

	for i in range(2):

		for sent_i in range(len(id_doc[i])):
			sent_emb = []
			word_emb_list = []  # list of a sentence's word embeddings
			# get word embeddings
			if WORD_REP == "glove":
				for wordID in id_doc[i][sent_i]:
					word_emb = nlp.vocab.get_vector(wordID)
					word_emb_list.append(word_emb)
			if WORD_REP == "elmo":
				sent_vec = MODEL.embed_batch([text_doc[i][sent_i]])
				sent_vec = sent_vec[0]  # 1 elt in batch
				word_emb_list = np.average(sent_vec, axis=0)  # average layers to get word embs
				# remove stopwords from elmo
				keep_inds = []
				for word_i in range(len(text_doc[i][sent_i])):
					word = text_doc[i][sent_i][word_i]
					# if the lower-cased word is a stop word or not alphabetic, remove it from emb and id
					if (word.isalpha()) and (word.lower() not in stop_words):
						keep_inds.append(word_i)
				word_emb_list = [word_emb_list[x] for x in range(len(text_doc[i][sent_i])) if x in keep_inds]
				id_doc[i][sent_i] = [id_doc[i][sent_i][x] for x in range(len(text_doc[i][sent_i])) if x in keep_inds]
				assert(len(word_emb_list) == len(id_doc[i][sent_i]))

			# add word embeddings to embedding dict
			if METRIC != "sms":
				for w_ind in range(len(word_emb_list)):
					# if the word is not already in the embedding dict, add it
					w_id = id_doc[i][sent_i][w_ind]
					if w_id not in rep_map:
						rep_map[w_id] = word_emb_list[w_ind]
					# for contextualized embeddings, replace word ID with a unique ID and add it to the embedding dict
					elif WORD_REP != "glove":
						rep_map[new_id] = word_emb_list[w_ind]
						id_doc[i][sent_i][w_ind] = new_id
						new_id += 1

			# add sentence embeddings to embedding dict
			if (METRIC != "wms") and (len(word_emb_list) > 0):
				sent_emb = get_sent_embedding(word_emb_list)
				# add sentence embedding to the embedding dict
				rep_map[new_id] = sent_emb
				sent_ids[i].append(new_id)
				new_id += 1

	# add sentence IDs to ID list
	if METRIC != "wms":
		for j in range(len(id_doc)):
			id_doc[j].append(sent_ids[j])

	return id_doc, rep_map


def get_sent_embedding(emb_list):

	# input: list of a sentence's word embeddings
	# output: the sentence's embedding

	emb_array = np.array(emb_list)
	sent_emb = list(np.mean(emb_array, axis=0))

	return sent_emb


def get_weights(id_doc):

	# input: a ref/hyp pair, with each piece is a list of sentences and each sentence is a list of token IDs.
	#           if the metric is not wms, there is also an extra list of sentence ids for ref and hyp
	# output: 1. a ref/hyp pair of 1-d lists of all word and sentence IDs (where applicable)
	#           2. a ref/hyp pair of arrays of weights for each of those IDs

	# Note that we only need to output counts; these will be normalized by the sum of counts in the WMD code.

	# 2 1-d lists of all relevant embedding IDs
	id_lists = [[], []]
	# 2 arrays where an embedding's weight is at the same index as its ID in id_lists
	d_weights = [np.array([], dtype=np.float32), np.array([], dtype=np.float32)]

	for i in range(len(id_doc)):  # for ref/hyp
		if METRIC != "wms":
			# pop off sent ids so id_doc is back to word ids only
			sent_ids = id_doc[i].pop()

		# collapse to 1-d
		wordIDs = sum(id_doc[i], [])
		# get dict that maps from ID to count
		counts = Counter(wordIDs)

		# get word weights
		if METRIC != "sms":
			for k in counts.keys():
				id_lists[i].append(k)
				d_weights[i] = np.append(d_weights[i], counts[k])

		# get sentence weights
		if METRIC != "wms":
			# weight words by counts and give each sentence a weight equal to the number of words in the sentence
			id_lists[i] += sent_ids
			# make sure to check no empty ids
			d_weights[i] = np.append(d_weights[i], np.array([float(len(x)) for x in id_doc[i] if x != []], dtype=np.float32))

	return id_lists, d_weights

def score_list(results_list):
	res = []
	for i in range(len(results_list)):
		ref_str = results_list[i][0][0]
		hyp_str = results_list[i][0][1]
		dict = {'id':i, 'ref':ref_str, 'hyp':hyp_str.strip("\n"), 'score':results_list[i][1]}
		res.append(dict)
	return res


def calc_smd(inLines, model):
	global nlp
	nlp = model
	#print("Found", len(inLines), "documents")
	# TODO: rewrite this
	token_doc_list, text_doc_list = tokenize_texts(inLines)
	results_list = []
	for doc_id in range(len(token_doc_list)):
		doc = token_doc_list[doc_id]
		# TODO: rewrite this
		text = text_doc_list[doc_id]
		# transform doc to ID list, both words and/or sentences. get ID dict that maps to emb
		# TODO: rewrite this
		try:
			[ref_ids, hyp_ids], rep_map = get_embeddings(doc, text)
		except ValueError:
			print(inLines[doc_id])
			print('ValueError: max() arg is an empty sequence; get_embeddings')
			continue
		# get D values
		[ref_id_list, hyp_id_list], [ref_d, hyp_d] = get_weights([ref_ids, hyp_ids])
		# format doc as expected: {id: (id, ref_id_list, ref_d)}
		doc_dict = {"0": ("ref", ref_id_list, ref_d), "1": ("hyp", hyp_id_list, hyp_d)}
		calc = WMD(rep_map, doc_dict, vocabulary_min=1)
		try:
			dist = calc.nearest_neighbors(str(0), k=1, early_stop=1)[0][1]  # how far is hyp from ref?
			sim = math.exp(-dist)  # switch to similarity
		except IndexError:
			print('dist = calc.nearest_neighbors(str(0), k=1, early_stop=1)[0][1]')
			print('IndexError: list index out of range')
			print(inLines[doc_id])
			continue
		except UnboundLocalError:
			print('dist could not be calculated')
			print(inLines[doc_id])
			continue
		except ValueError:
			print('Too little vocabulary')
			print(inLines[doc_id])
			continue

		results_list.append((inLines[doc_id],sim))

	return score_list(results_list)
