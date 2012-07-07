(ns stewie.app
  (use stewie.core
       stewie.crypto
       stewie.db
       noir.core
       somnium.congomongo)
  (:require [noir.server :as server]
            [noir.response :as response]))

(def detect (bucket-detector))

(defpage "/" []
  "Welcome to Stewie!\n")

(defn convert-to-numbers
  "convert hash-map values to numbers"
  [h]
  (into {} (map (fn [[k v]] [k (read-string v)]) h)))

(defpage "/:bucket" {bucket :bucket}
  (let [new-token (token bucket)]
    (response/json {:token new-token})))

(defpage [:post "/:bucket"] {bucket :bucket :as data}
  (let [data (dissoc data :bucket)
        data (convert-to-numbers data)
        density (detect bucket data)
        data {:data data :density density}
        id (save-data :stewie bucket data)]
    (response/json data)))

(defn -main [& m]
  (let [mode (keyword (or (first m) :dev))
        port (Integer. (get (System/getenv) "PORT" "8080"))]
    (server/start port {:mode mode :ns 'stewie})))
