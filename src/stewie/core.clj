(ns stewie.core)

(defn accumulator
  "Generages an accumulator that will return average and variance in O(1)

  It keeps an internal state of:
  {
    :total sum(x_i),
    :sq_total sum(x_i ^ 2),
    :count count(x_i),
  }

  Result is:
  {
    :average      :total / :count
    :variance     :sq_total / :count - :average ^ 2
  }

  "
  []
  (let [totals (atom {:total 0, :count 0, :sq_total 0})]
    (fn [n]
      (let [update_totals (comp #(update-in % [:count] inc)
                                #(update-in % [:total] + n)
                                #(update-in % [:sq_total] + (Math/pow n 2)))
            result (swap! totals update_totals)
            cnt (result :count)
            avg (/ (result :total) cnt)]
        {:average avg
         :variance (- (/ (result :sq_total) cnt) (Math/pow avg 2))}))))

; See http://en.wikipedia.org/wiki/Probability_density_function
(defn density
  "Calculates probability density function"
  [x average variance]
  (let [sigma (Math/sqrt variance)
        divisor (* sigma (Math/sqrt (* 2 Math/PI)))
        exponent (/ (Math/pow (- x average) 2) (* 2 variance))]
    (/ (Math/exp (- exponent)) divisor)))

(defn single-variable-detector
  "Given an stream input of values, returns the probability density for the last input"
  []
  (let [acc (accumulator)]
    (fn [x]
      (let [state (acc x)]
        (density x (state :average) (state :variance))))))

(defn atom-hash-map
  "Returns a function that receives a key and returns a value for that key.

  If the key is new, uses the default-creator to generate a new value"
  [default-creator]
  (let [a (atom {})]
    (fn [x]
      (let [add-key (fn [k] (swap! a #(assoc-in % [k] (default-creator))))
            get-key (fn [k] (if (contains? @a k) (@a k) ((add-key k) k)))]
        (get-key x)))))

(defn detector
  "Given an stream input of points as maps, returns the probability density for the last point"
  []
  (let [detectors (atom-hash-map single-variable-detector)]
    (fn [x]
      (let [get-var-density (fn [kv] (let [[k v] kv] ((detectors k) v)))
            densities (map get-var-density x)]
        (reduce * densities)))))

(defn bucket-detector
  "Returns a function that will create one detector per key (bucket)"
  []
  (let [detectors (atom-hash-map detector)]
    (fn [bucket x]
      (let [det (detectors bucket)]
        (det x)))))

; Reference implementations
(defn average
  "naive average implementation"
  [coll]
  (/ (reduce + coll) (count coll)))

(defn variance
  "naive variance implementation"
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
