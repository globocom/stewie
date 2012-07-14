(ns stewie.db
  (:use somnium.congomongo
        [somnium.congomongo.config :only [*mongo-config*]]))

;MongoDB setup functions taken from http://thecomputersarewinning.com/post/clojure-heroku-noir-mongo/

(defn split-mongo-url
  "Parses mongodb url from heroku, eg. mongodb://user:pass@localhost:1234/db"
  [url]
  (let [matcher (re-matcher #"^.*://(.*?):(.*?)@(.*?):(\d+)/(.*)$" url)] ;; Setup the regex.
    (when (.find matcher) ;; Check if it matches.
      (zipmap [:match :user :pass :host :port :db] (re-groups matcher))))) ;; Construct an options map.

(defn maybe-init
  "Checks if connection and collection exist, otherwise initialize."
  [collection]
  (when (not (connection? *mongo-config*)) ;; If global connection doesn't exist yet.
    (let [mongo-url (get (System/getenv) "MONGOHQ_URL" "mongodb://:@localhost:27017/stewie") ;; Heroku puts it here.
          config    (split-mongo-url mongo-url)] ;; Extract options.
      (println "Initializing mongo @ " mongo-url)
      (mongo! :db (:db config) :host (:host config) :port (Integer. (:port config))) ;; Setup global mongo.
      (authenticate (:user config) (:pass config)) ;; Setup u/p.
      (or (collection-exists? collection) ;; Create collection named 'firstcollection' if it doesn't exist.
          (create-collection! collection)))))

(defn save-data
  "Posts information to mongo"
  [collection bucket data]
    (insert! collection (assoc data :bucket bucket)))

(defn has-data
  "Checks if there is data for bucket in mongo"
  [collection bucket]
    (> (fetch-count collection :where {:bucket bucket}) 0))
