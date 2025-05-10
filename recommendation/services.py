import numpy as np
from transformers import BertTokenizer, BertModel
import torch
from django.conf import settings
from hotels.models import Room

class RecommendationEngine:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained(settings.RECOMMENDATION_SETTINGS['MODEL_PATH'])
        self.model = BertModel.from_pretrained(settings.RECOMMENDATION_SETTINGS['MODEL_PATH'])
    
    def generate_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=100)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()
    
    def similarity_score(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def get_recommendations(self, target_room, user):
        all_rooms = Room.objects.exclude(id=target_room.id).prefetch_related('hotel')
        
        scores = []
        target_vec = np.array(target_room.search_vector)
        
        for room in all_rooms:
            if not room.search_vector:
                continue
                
            # Score de similarité
            content_score = self.similarity_score(target_vec, np.array(room.search_vector))
            
            # Score de popularité
            popularity_score = np.log(room.booking_count + 1) if room.booking_count else 0
            
            # Score combiné
            total_score = 0.7 * content_score + 0.3 * popularity_score
            
            if total_score > settings.RECOMMENDATION_SETTINGS['MIN_SIMILARITY']:
                scores.append((room, total_score))
        
        # Trier et retourner les meilleurs résultats
        scores.sort(key=lambda x: x[1], reverse=True)
        return [room for room, score in scores[:settings.RECOMMENDATION_SETTINGS['MAX_RECOMMENDATIONS']]]