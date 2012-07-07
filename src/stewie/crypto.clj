(ns stewie.crypto)

(def secret (get (System/getenv) "SECRET" "SECRET"))

(defn token
  ([bucket]
    (let [algorithm "HmacSHA1"
          encoding "ASCII"
          secret (javax.crypto.spec.SecretKeySpec. (.getBytes secret encoding) algorithm)
          mac (doto (javax.crypto.Mac/getInstance algorithm)
                    (.init secret))
          bytes (.doFinal mac (.getBytes bucket encoding))]
      (format "%x" (.abs (new java.math.BigInteger bytes))))))
