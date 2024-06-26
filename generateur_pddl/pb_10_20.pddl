(define (problem pb-10cities)
    (:domain domain)
    (:requirements :strips)
    (:objects c0 c1 c2 c3 c4 c5 c6 c7 c8 c9)
    (:init (connected c0 c1) (connected c0 c2) (connected c0 c3) (connected c0 c4) (connected c0 c7) (connected c1 c0) (connected c1 c2) (connected c1 c3) (connected c1 c5) (connected c1 c9) (connected c2 c0) (connected c2 c1) (connected c2 c5) (connected c2 c6) (connected c2 c8) (connected c3 c0) (connected c3 c1) (connected c3 c6) (connected c3 c9) (connected c4 c0) (connected c4 c5) (connected c5 c1) (connected c5 c2) (connected c5 c4) (connected c5 c7) (connected c5 c9) (connected c6 c2) (connected c6 c3) (connected c6 c7) (connected c6 c8) (connected c7 c0) (connected c7 c5) (connected c7 c6) (connected c8 c2) (connected c8 c6) (connected c8 c9) (connected c9 c1) (connected c9 c3) (connected c9 c5) (connected c9 c8) (in c0) (not (delivered c0)) (not (in c1)) (not (in c2)) (not (in c3)) (not (in c4)) (not (in c5)) (not (in c6)) (not (in c7)) (not (in c8)) (not (in c9)))     
    (:goal (and (in c0) (delivered c0) (delivered c1) (delivered c2) (delivered c3) (delivered c4) (delivered c5) (delivered c6) (delivered c7) (delivered c8) (delivered c9)))
)