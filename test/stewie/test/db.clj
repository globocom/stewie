(ns stewie.test.db
  (:use stewie.db
        somnium.congomongo
        midje.sweet))

(fact "mongo connection works"
  (let [db (maybe-init :test)]
    (insert! :test {:foo "bar"})
    (collection-exists? :test) => true))

(fact "save-data persists data on mongo"
  (let [db (maybe-init :test)
        data {:x 10 :y 20}
        bucket :any
        return-value (save-data :test bucket data)]
    (return-value :data) => data
    ((fetch-one :test :where {:_id (return-value :_id)}) :bucket) => "any"))
