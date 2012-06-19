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

(defn sliding-window-average
  "calculates the average of the first n elements of coll"
  [coll n]
  (average (take n coll)))

(defn sliding-window-variance
  "calculates the variance of the first n elements of coll"
  [coll n]
  (variance (take n coll)))
