

(defmacro with-open-files (args &body body)
  (case (length args)
    ((0)
     `(progn ,@body))
    ((1)
     `(with-open-file ,(first args) ,@body))
    (t `(with-open-file ,(first args)
	  (with-open-files
	      ,(rest args) ,@body)))))


(with-open-files ((fo "/Users/ar/work/MorphoBr/tmp/dicc-AO3_long-1pl.src"
		      :direction :output :if-exists :supersede)
		  (fi "/Users/ar/work/MorphoBr/tmp/dicc-AO3_long.src"))
  (do ((line (read-line fi nil nil)
	     (read-line fi nil nil)))
      ((null line))
    (let ((reg (cl-ppcre:split "[ ]+" line)))
      (dotimes (i (/ (1- (length reg)) 2))
	(format fo "~a ~a ~a~%" (car reg) (nth (+ 1 (* i 2)) reg) (nth (+ 2 (* i 2)) reg))))))

