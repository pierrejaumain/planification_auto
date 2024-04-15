(define (problem pb-20cities)
    (:domain domain)
    (:requirements :strips)
    (:objects c0 c1 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c2 c3 c4 c5 c6 c7 c8 c9)
    (:init (connected c0 c1) (connected c0 c12) (connected c0 c19) (connected c0 c2) (connected c0 c3) (connected c0 c8) (connected c0 c9) (connected c1 c0) (connected c1 c12) (connected c1 c14) (connected c1 c17) (connected c10 c13) (connected c10 c14) (connected c10 c16) (connected c10 c17) (connected c10 c19) (connected c10 c4) (connected c10 c5) (connected c10 c8) (connected c11 c12) (connected c11 c15) (connected c11 c5) (connected c12 c0) (connected c12 c1) (connected c12 c11) (connected c12 c14) (connected c12 c3) (connected c12 c6) (connected c12 c9) (connected c13 c10) (connected c13 c14) (connected c13 c15) (connected c13 c16) (connected c13 c8) (connected c14 c1) (connected c14 c10) (connected c14 c12) (connected c14 c13) (connected c14 c15) (connected c14 c19) (connected c14 c3) (connected c14 c9) (connected c15 c11) (connected c15 c13) (connected c15 c14) (connected c15 c16) (connected c15 c7) (connected c16 c10) (connected c16 c13) (connected c16 c15) (connected c16 c2) (connected c16 c3) (connected c16 c5) (connected c17 c1) (connected c17 c10) (connected c17 c4) (connected c17 c9) (connected c18 c2) (connected c19 c0) (connected c19 c10) (connected c19 c14) (connected c19 c3) (connected c19 c6) (connected c2 c0) (connected c2 c16) (connected c2 c18) (connected c2 c4) (connected c2 c5) (connected c3 c0) (connected c3 c12) (connected c3 c14) (connected c3 c16) (connected c3 c19) (connected c3 c6) (connected c3 c7) (connected c3 c9) (connected c4 c10) (connected c4 c17) (connected c4 c2) (connected c4 c6) (connected c5 c10) (connected c5 c11) (connected c5 c16) (connected c5 c2) (connected c6 c12) (connected c6 c19) (connected c6 c3) (connected c6 c4) (connected c6 c8) (connected c7 c15) (connected c7 c3) (connected c8 c0) (connected c8 c10) (connected c8 c13) (connected c8 c6) (connected c9 c0) (connected c9 c12) (connected c9 c14) (connected c9 c17) (connected c9 c3) (in c0) (not (delivered c0)) (not (in c1)) (not (in c10)) (not (in c11)) (not (in c12)) (not (in c13)) (not (in c14)) (not (in c15)) (not (in c16)) (not (in c17)) (not (in c18)) (not (in c19)) (not (in c2)) (not (in c3)) (not (in c4)) (not (in c5)) (not (in c6)) (not (in c7)) (not (in c8)) (not (in c9)))
    (:goal (and (in c0) (delivered c0) (delivered c1) (delivered c2) (delivered c3) (delivered c4) (delivered c5) (delivered c6) (delivered c7) (delivered c8) (delivered c9) (delivered c10) (delivered c11) (delivered c12) (delivered c13) (delivered c14) (delivered c15) (delivered c16) (delivered c17) (delivered c18) (delivered c19)))
)