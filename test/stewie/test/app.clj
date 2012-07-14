(ns stewie.test.app
  (:use stewie.app
        stewie.core
        stewie.crypto
        stewie.db
        stewie.test.db
        midje.sweet)
  (:require [cheshire.core :as json]
            [noir.util.test :as noir]
            [somnium.congomongo :as mongo]))

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
  (let [initiated (maybe-init collection)
        cleaned (clean-bucket! collection :temp)
        response (noir/send-request [:post "/temp"] {"x" "1"})
        fetch-count (mongo/fetch-count collection :where {:bucket :temp})]
    fetch-count => 1))

(fact "get to bucket returns token"
  (let [initiated (maybe-init collection)
        cleaned (clean-bucket! collection :token)
        response (noir/send-request "/token")]
    (response :status) => 200
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "token") => (token "token")))

(fact "get to bucket does not return token if it is already taken"
  (let [initiated (maybe-init collection)
        cleaned (clean-bucket! collection :token)
        response (noir/send-request [:post "/token"] {"x" "1"})
        response (noir/send-request "/token")]
    (response :status) => 410
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "error") => "token already taken"))
