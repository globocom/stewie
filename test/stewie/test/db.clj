(ns stewie.test.db
  (:use stewie.db
        somnium.congomongo
        midje.sweet))

(defn clean-bucket! [collection bucket]
  (seq (for [id (fetch collection :where {:bucket bucket})]
    (destroy! collection id))))

(fact "mongo connection works"
  (let [db (maybe-init :test)]
    (insert! :test {:foo "bar"})
    (collection-exists? :test) => true))

(fact "save-data persists data on mongo"
  (let [db (maybe-init :test)
        data {:x 10 :y 20}
        density 1.2
        full-data {:data data :density density}
        bucket :any
        return-value (save-data :test bucket full-data)]
    (return-value :data) => data
    (return-value :density) => density
    ((fetch-one :test :where {:_id (return-value :_id)}) :bucket) => "any"))

(fact "has-data returns false for new bucket"
  (let [db (maybe-init :test)
        bucket :unused
        cleaned (clean-bucket! :test bucket)]
    (has-data :test bucket) => false))

(fact "has-data returns true for used bucket"
  (let [db (maybe-init :test)
        bucket :used
        cleaned (clean-bucket! :test bucket)
        saved (save-data :test bucket {})]
    (has-data :test bucket) => true))
