import csv
from datasketch import MinHash, MinHashLSH
import generar_nuevo_archivo_tweets

def generar_diccionario_desde_csv(archivo_csv):
    tweets_per_person = {}

    with open(archivo_csv, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            screen_name = row['screen_name']
            tweet_text = row['text']

            if screen_name not in tweets_per_person:
                tweets_per_person[screen_name] = []

            tweets_per_person[screen_name].append(tweet_text)

    return tweets_per_person

def k_shingles(tweet, k):
    shingles = set()
    for i in range(len(tweet) - k):
        shingle = tweet[i:i+k]
        shingles.add(shingle)
    return shingles

def process_tweets(tweets_per_person):
    minhashes = {}
    lsh = MinHashLSH(threshold=0.9)
    
    for person, tweets in tweets_per_person.items():
        minhash = MinHash(num_perm=128)
        for tweet in tweets:
            shingles = k_shingles(tweet, 3)
            for shingle in shingles:
                minhash.update(shingle.encode('utf-8'))

        minhashes[person] = minhash
        lsh.insert(person, minhash)

    return minhashes, lsh

def find_similar_pairs(tweets_per_person, minhashes, lsh):
    similar_pairs = []
    pairs = set()

    for person, _ in tweets_per_person.items():
        minhash = minhashes[person]
        candidates = lsh.query(minhash)
        candidates.remove(person)

        for candidate in candidates:
            candidate_minhash = minhashes[candidate]
            similarity = minhash.jaccard(candidate_minhash)
            if similarity >= 0.9:
                if (candidate, person) not in pairs:
                    similar_pairs.append((person, candidate))
                    pairs.add((person, candidate))

    return similar_pairs

def escribir_csv(similar_pairs, archivo_salida):
    with open(archivo_salida, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['persona1', 'persona2'])
        writer.writerows(similar_pairs)

def main():

    archivo_entrada = 'tweets_2022_abril_junio.csv'
    archivo_salida = 'tweets.csv'
    datos = generar_nuevo_archivo_tweets.leer_csv(archivo_entrada)
    generar_nuevo_archivo_tweets.escribir_csv(datos, archivo_salida)
    print("Las 2000000 primeras líneas se han escrito en el archivo 'tweets.csv'.")

    grupos_similares = 'parejas_similares_v1.csv'
    tweets_per_person = generar_diccionario_desde_csv(archivo_salida)
    minhashes, lsh = process_tweets(tweets_per_person)
    similar_pairs = find_similar_pairs(tweets_per_person, minhashes, lsh)
    escribir_csv(similar_pairs, grupos_similares)
    print("El archivo ha terminado de ejecutarse!")

if __name__ == '__main__':
    main()