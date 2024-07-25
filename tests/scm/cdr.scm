(begin
  (define cons (lambda (x y)
                (lambda (m)
                  (if (str= m "car")
                    x
                    (if (str= m "cdr")
                      y
                      (throw "Error"))))))

  (define car (lambda (z) (z "car")))

  (define cdr (lambda (z) (z "cdr")))
  (cdr (cons "left" "right")))
