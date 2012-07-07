(ns stewie.test.app
  (:use stewie.app
        stewie.core
        stewie.crypto
        stewie.db
        midje.sweet)
  (:require [cheshire.core :as json])
  (:require [noir.util.test :as noir])
  (:require [somnium.congomongo :as mongo]))

(fact "homepage returns status 200"
  (-> (noir/send-request "/") :status) => 200)

(fact "post to bucket returns json"
  (let [response (noir/send-request [:post "/bucket"] {"x" "1"})]
    (response :status) => 200
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "density") => "NaN"))

(fact "post to bucket has memory"
  (noir/with-noir
    (let [input (range 11)
          post-to-bucket (fn [x] (noir/send-request [:post "/memory"] {"x" (str x)}))
          response (last (for [x input] (post-to-bucket x)))
          json-response (json/parse-string (response :body))]
      (json-response "density") => (density (last input) (average input) (variance input)))))

(fact "post to bucket persists data on mongo"
  (let [initiated (maybe-init :stewie)
        destroyed (seq (for [id (mongo/fetch :stewie :where {:bucket :temp})] (mongo/destroy! :stewie id)))
        response (noir/send-request [:post "/temp"] {"x" "1"})
        fetch-count (mongo/fetch-count :stewie :where {:bucket :temp})]
    fetch-count => 1))

(fact "get to bucket returns token"
  (let [response (noir/send-request "/token")]
    (response :status) => 200
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "token") => (token "token")))
