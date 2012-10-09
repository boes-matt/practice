;; Code from The Little Schemer by Friedman and Felleisen
;; Use the Pretty Big language in DrRacket

;; Chapters 1-4

(require (lib "trace.ss"))

(define atom?
  (lambda (x)
    (and (not (pair? x)) (not (null? x)))))

(define lat?
  (lambda (lst)
    (cond
      ((null? lst) #t)
      ((atom? (car lst)) (lat? (cdr lst)))
      (else #f))))

(define member?
  (lambda (a lst)
    (cond
      ((null? lst) #f)
      ((eq? a (car lst)) #t)
      (else (member? a (cdr lst))))))

(define rember
  (lambda (a lst)
    (cond
      ((null? lst) '())
      ((eq? a (car lst)) (cdr lst))
      (else (cons (car lst) (rember a (cdr lst)))))))

(define rember-all
  (lambda (a lst)
    (cond
      ((null? lst) '())
      ((eq? a (car lst)) (rember-all a (cdr lst)))
      (else (cons (car lst) (rember-all a (cdr lst)))))))

(define firsts
  (lambda (lst)
    (cond
      ((null? lst) '())
      (else (cons (car (car lst)) (firsts (cdr lst)))))))

(define seconds
  (lambda (lst)
    (cond
      ((null? lst) '())
      (else (cons (cadar lst) (seconds (cdr lst)))))))

(define insertR
  (lambda (new old lst)
    (cond
      ((null? lst) '())
      ((eq? (car lst) old) (cons (car lst) (cons new (cdr lst))))
      (else (cons (car lst) (insertR new old (cdr lst)))))))

(define insertL
  (lambda (new old lst)
    (cond
      ((null? lst) '())
      ((eq? (car lst) old) (cons new lst))
      (else (cons (car lst) (insertL new old (cdr lst)))))))

(define subst
  (lambda (new old lst)
    (cond
      ((null? lst) '())
      ((eq? (car lst) old) (cons new (cdr lst)))
      (else (cons (car lst) (subst new old (cdr lst)))))))

(define subst2
  (lambda (new old1 old2 lst)
    (cond
      ((null? lst) '())
      ((or (eq? (car lst) old1) (eq? (car lst) old2)) (cons new (cdr lst)))
      (else (cons (car lst) (subst2 new old1 old2 (cdr lst)))))))

(define multirember
  (lambda (a lst)
    (cond
      ((null? lst) '())
      ((eq? a (car lst)) (multirember a (cdr lst)))
      (else (cons (car lst) (multirember a (cdr lst)))))))

(define multiinsertR
  (lambda (new old lst)
    (cond
      ((null? lst) '())
      ((eq? (car lst) old) (cons old (cons new (multiinsertR new old (cdr lst)))))
      (else (cons (car lst) (multiinsertR new old (cdr lst)))))))

(define multiinsertL
  (lambda (new old lst)
    (cond
      ((null? lst) '())
      ((eq? (car lst) old) (cons new (cons old (multiinsertL new old (cdr lst)))))
      (else (cons (car lst) (multiinsertL new old (cdr lst)))))))

(define multisubst
  (lambda (new old lst)
    (cond
      ((null? lst) '())
      ((eq? (car lst) old) (cons new (multisubst new old (cdr lst))))
      (else (cons (car lst) (multisubst new old (cdr lst)))))))

(define o+
  (lambda (n m)
    (cond
      ((zero? m) n)
      (else (add1 (o+ n (sub1 m)))))))

;; tail recursive version of o+
;; no need maintain chain of stack frames
(define oo+
  (lambda (n m)
    (cond      
      ((zero? m) n)
      (else (oo+ (add1 n) (sub1 m))))))

(define o-
  (lambda (n m)
    (cond
      ((zero? m) n)
      (else (sub1 (o- n (sub1 m)))))))

(define addtup
  (lambda (tup)
    (cond
      ((null? tup) 0)
      (else (o+ (car tup) (addtup (cdr tup)))))))

(define x
  (lambda (n m)
    (cond
      ((zero? m) 0)
      (else (o+ n (x n (sub1 m)))))))

(define tup+
  (lambda (tup1 tup2)
    (cond
      ((null? tup1) tup2)
      ((null? tup2) tup1)
      (else (cons (o+ (car tup1) (car tup2)) (tup+ (cdr tup1) (cdr tup2)))))))

(define o>
  (lambda (n m)
    (cond
      ((zero? n) #f)
      ((zero? m) #t)
      (else (o> (sub1 n) (sub1 m))))))

(define o<
  (lambda (n m)
    (cond
      ((zero? m) #f)
      ((zero? n) #t)
      (else (o< (sub1 n) (sub1 m))))))
    
(define o=
  (lambda (n m)
    (cond
      ((and (zero? n) (zero? m)) #t)
      ((or (zero? n) (zero? m)) #f)
      (else (o= (sub1 n) (sub1 m))))))

(define oo=
  (lambda (n m)
    (cond
      ((zero? n) (zero? m))
      ((zero? m) #f)
      (else (oo= (sub1 n) (sub1 m))))))

(define ooo=
  (lambda (n m)
    (cond
      ((o< n m) #f)
      ((o> n m) #f)
      (else #t))))

(define ^
  (lambda (base exp)
    (cond
      ((zero? exp) 1)
      (else (x base (^ base (sub1 exp)))))))

(define div
  (lambda (n m)
    (cond
      ((zero? m) #f)
      ((< n m) 0)
      (else (add1 (div (- n m) m))))))

(define len
  (lambda (lst)
    (cond
      ((null? lst) 0)
      (else (add1 (len (cdr lst)))))))

(define pick
  (lambda (pos lst)
    (cond
      ((zero? (sub1 pos)) (car lst))
      (else (pick (sub1 pos) (cdr lst))))))

(define rempick
  (lambda (pos lst)
    (cond
      ((zero? (sub1 pos)) (cdr lst))
      (else (cons (car lst) (rempick (sub1 pos) (cdr lst)))))))

(define no-nums
  (lambda (lst)
    (cond
      ((null? lst) '())
      ((number? (car lst)) (no-nums (cdr lst)))
      (else (cons (car lst) (no-nums (cdr lst)))))))

(define all-nums
  (lambda (lst)
    (cond
      ((null? lst) '())
      ((number? (car lst)) (cons (car lst) (all-nums (cdr lst))))
      (else (all-nums (cdr lst))))))

(define eqan?
  (lambda (a1 a2)
    (cond
      ((and (number? a1) (number? a2)) (= a1 a2))
      ((or (number? a1) (number? a2)) #f)
      (else (eq? a1 a2)))))

(define occur
  (lambda (a lst)
    (cond
      ((null? lst) 0)
      ((eqan? a (car lst)) (add1 (occur a (cdr lst))))
      (else (occur a (cdr lst))))))

(define one?
  (lambda (n)
    (= n 1)))

(define rempick2
  (lambda (pos lst)
    (cond
      ((one? pos) (cdr lst))
      (else (cons (car lst) (rempick2 (sub1 pos) (cdr lst)))))))
