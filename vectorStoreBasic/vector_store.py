import numpy as np

'''
Setting up vectore store class to store each vector and it similarity to all others in the corpus
{
    'vec1': {
        'vec3': 0.974631846,
        'vec4': similarity_score_between_vec1_and_vec4
    },
    'vec2': {
        'vec3': 0.998190892,
        'vec4': similarity_score_between_vec2_and_vec4
}

'''

class VectorStore:
    def __init__(self) -> None:
        '''
        vector_data: dict stores vectors
        vector_index: dict stores index number per vector for retreival 
        '''
        self.vector_data = {}
        self.vector_index = {}

    def add_vector(self, vector_id, vector):
        '''
        Adds a vector to VectorStore.
        param: vector_id: str|int unique identifier for vector
        param: vector: numpy.narray vector to be stored
        '''
        self.vector_data[vector_id] = vector
        self.update_index(vector_id, vector)

    def get_vector(self, vector_id):
        '''
        Get a vector from VectorStore
        returns: numpy.ndarray vector if found, None if not found
        param: vector_id: str|int unique identifier for vector
        '''
        return self.vector_data.get(vector_id)
    
    def update_index(self, vector_id, vector):
        '''
        update the index for each new vector upon ingest
        vectore_id:  str|int unique identifier for vector
        vector: numpy.narray vector to be stored
        '''
        for existing_id, existing_vector in self.vector_data.items():
            similarity = np.dot(vector, existing_vector) / (np.linalg.norm(vector)) * (np.linalg.norm(existing_vector))
            if existing_id not in self.vector_index:
                self.vector_index[existing_id] = {}
            self.vector_index[existing_id][vector_id] = similarity

    def find_similar_vectors(self, query_vector, num_results=5):
        '''
        find nearest vectors to the query vector i.e. nearest neighbors.
        returns: list of tuples (vector_id, similarity_score) for similar vectors.
        param: query_vector: numpy.narray vector to find similar vectors to.
        param: num_results: int: number of nearest neighbors to return.
        '''
        results = []
        for vector_id, vector in self.vector_data.items():
            # TODO Fix RuntimeWarning: invalid value encountered in scalar divide
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            results.append((vector_id, similarity))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:num_results]