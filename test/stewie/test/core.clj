(ns stewie.test.core
  (:use [stewie.core])
  (:use midje.sweet))


(fact "average works"
	(average (repeat 10 1)) => 1
	(average (range 11)) => 5)

(fact "variance works"
	(variance (repeat 10 1)) => 0.0
	(variance [1 2 3 4 5]) => 2.0
	(variance [1 2 3 4]) => 1.25)
