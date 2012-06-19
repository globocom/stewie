(ns stewie.core)

(defn average
	"naive average implementation"
	[coll]
	(/ (reduce + coll) (count coll)))

(defn variance
	"naive variance deviation implementation"
	[coll]
	(let [avg (average coll)]
		 (/ (reduce + (map #(Math/pow (- % avg) 2) coll))
		 	(count coll))))