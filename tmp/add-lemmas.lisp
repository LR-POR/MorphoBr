(ql:quickload '(cl-conllu cl-ppcre alexandria split-sequence))

(defpackage :add-lemmas
  (:use :cl :cl-conllu :cl-ppcre :alexandria :split-sequence))

(in-package :add-lemmas)

;; ababadam        ababadar+V+PRS+3+PL

(defparameter *ud-conversion* (pairlis '("ADJ" "ADV" "AUX" "NOUN" "VERB") '("A" "ADV" "V" "N" "V")))

(defun morphobr-pos (udpos)
  (cdr (assoc udpos *ud-conversion* :test #'equal)))

(defun load-morphobr-dict (file)
  "Load dictionary in MorphoBr format and creates a hash-table of hash-tables.  First level are the forms and second level are the POS.  Each pos will have a list of (LEMMA + FEATS).  Example:

ADD-LEMMAS> (hash-table-alist (gethash 'andar' dict))
(('V' ('andar' 'INF' '3' 'SG') 
      ('andar' 'INF' '1' 'SG') 
      ('andar' 'INF')
      ('andar' 'SBJF' '3' 'SG')
      ('andar' 'SBJF' '1' 'SG'))
 ('N' ('andar' 'M' 'SG')))"
  (flet ((add-to-dictionary (dict form lemma pos feats)
           (let ((form-dict (ensure-gethash form dict (make-hash-table :test #'equal))))
             (push (cons lemma feats) (gethash pos form-dict)))))
    (let ((dictionary (make-hash-table :test #'equal)))
      (with-open-file (s file :direction :input)
        (do ((line (read-line s nil nil)
                   (read-line s nil nil)))
            ((null line))
          (let* ((split-line (split-sequence #\tab line))
                 (form (first split-line))
                 (lemma-tags (split-sequence #\+ (second split-line)))
                 (lemma (first lemma-tags))
                 (pos (second lemma-tags))
                 (feats (cddr lemma-tags)))
            (add-to-dictionary dictionary form lemma pos feats))))
      dictionary)))

(defun get-lemmas (form pos dict)
  (when (gethash form dict)
    (remove-duplicates (mapcar #'first (gethash pos (gethash form dict))) :test #'equal)))

(defun fill-lemmas (conllu dict stats-file)
  (with-open-file (ss stats-file :direction :output :if-exists :supersede)
    (mapc (lambda (s)
            (mapc (lambda (tk)
                    (let* ((mpos (morphobr-pos (token-upostag tk)))
                           (lemmas (get-lemmas (string-downcase (token-form tk)) mpos dict)))
                      (when mpos
                        (if lemmas
                            (if (= 1 (length lemmas))
                                (progn
                                  (if (string-equal (first lemmas) (token-lemma tk))
                                      (format ss "single eq: ~a (~a) [~a]~%" (token-form tk) (first lemmas) mpos)
                                      (format ss "single ne: ~a (~a, original: ~a) [~a]~%" (token-form tk) (first lemmas) (token-lemma tk) mpos))
                                  (setf (token-lemma tk) (first lemmas)))
                                (progn
                                  (format ss "multiple: ~a (~{~a~^ ~}) [~a]~%" (token-form tk) lemmas mpos)))
                            (format ss "missing: ~a [~a]~%" (token-form tk) mpos)))))
                  (sentence-tokens s))) conllu)))

(defun process-file (dict file-in file-out stats-file)
  "Using the dictionary DICT, fill the lemmas of file FILE-IN,
saving it on FILE-OUT while generating statistics about the lemmas in
STATS-FILE.  The statistics file contains one line per lemma processed
with the following status: 'single eq' means that the lemma in
DICT-FILE is the same as the one already in FILE-IN; 'single ne' means
that the lemma is different; 'multiple' means that multiple lemmas are
possible for that particular word form; 'missing' means that we didn't
find an entry for that particular word form in our dictionary."
  (write-conllu (fill-lemmas (read-conllu file-in) dict stats-file) file-out))

;; if using SBCL, you need at least 16 gb of memory:
;; sbcl --dynamic-space-size 16gb --load add-lemmas.lisp
(dolist (f (directory "*.conllu"))
  (let ((dict (load-morphobr-dict "dict")))
      (sb-ext:gc)
      (process-file dict f (format nil "~a.l" f) (format nil "~a.s" f))))

(sb-ext:exit)
