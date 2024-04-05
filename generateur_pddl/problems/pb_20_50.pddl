(define (problem pb-20cities_50edges)
    (:domain tps)
    (:requirements :strips)
    (:objects c0 c1 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c2 c3 c4 c5 c6 c7 c8 c9)
    (:init (connected c0 c1) (connected c0 c11) (connected c0 c3) (connected c1 c10) (connected c1 c14) (connected c1 c15) (connected c1 c16) (connected c1 c2) (connected c1 c4) (connected c1 c5) (connected c1 c9) (connected c11 c13) (connected c12 c16) (connected c12 c18) (connected c12 c19) (connected c13 c17) (connected c13 c18) (connected c14 c17) (connected c15 c18) (connected c16 c17) (connected c17 c18) (connected c18 c19) (connected c2 c15) (connected c2 c17) (connected c2 c5) (connected c2 c7) (connected c2 c8) (connected c3 c11) (connected c3 c12) (connected c3 c14) (connected c3 c8) (connected c4 c12) (connected c4 c19) (connected c4 c7) (connected c5 c10) (connected c5 c11) (connected c5 c13) (connected c5 c16) (connected c5 c6) (connected c5 c8) (connected c5 c9) (connected c6 c12) (connected c7 c11) (connected c7 c14) (connected c7 c16) (connected c8 c10) (connected c8 c11) (connected c8 c9) (connected c9 c13) (connected c9 c17) (in c0) (not (delivered c0)) (not (in c1)) (not (in c10)) (not (in c11)) (not (in c12)) (not (in c13)) (not (in c14)) (not (in c15)) (not (in c16)) (not (in c17)) (not (in c18)) (not (in c19)) (not (in c2)) (not (in c3)) (not (in c4)) (not (in c5)) (not (in c6)) (not (in c7)) (not (in c8)) (not (in c9)))
    (:goal (and (in c0) (delivered c0) (delivered c1) (delivered c2) (delivered c3) (delivered c4) (delivered c5) (delivered c6) (delivered c7) (delivered c8) (delivered c9) (delivered c10) (delivered c11) (delivered c12) (delivered c13) (delivered c14) (delivered c15) (delivered c16) (delivered c17) (delivered c18) (delivered c19)))
)