(ns stewie.app
  (:use stewie.core)
  (:use noir.core)
  (:require [noir.server :as server]
            [noir.response :as response]))

(def detect (detector))

(defpage "/" []
  "Welcome to Stewie!\n")

(defn convert-to-numbers
  "convert hash-map values to numbers"
  [h]
  (into {} (map (fn [[k v]] [k (read-string v)]) h)))

(defpage [:post "/"] {:as data}
  (let [data (convert-to-numbers data)
        data (assoc data :density (detect data))]
    (response/json data)))

(defn -main [& m]
  (let [mode (keyword (or (first m) :dev))
        port (Integer. (get (System/getenv) "PORT" "8080"))]
    (server/start port {:mode mode :ns 'stewie})))
