(ns stewie.test.app
  (:use [stewie.app])
  (:use [midje.sweet])
  (:require [cheshire.core :as json])
  (:require [noir.util.test :as noir]))

(fact "homepage returns status 200"
  (-> (noir/send-request "/") :status) => 200)

(fact "post to bucket returns json"
  (let [response (noir/send-request [:post "/bucket"])]
    (response :status) => 200
    ((response :headers) "Content-Type") => "application/json"
    ((json/parse-string (response :body)) "density") => 1))
