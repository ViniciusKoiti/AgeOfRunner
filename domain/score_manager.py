from typing import Dict, List
import json
import os

class ScoreManager:
    def __init__(self, scores_file: str):
        self.scores_file = scores_file
        self.high_scores = self.load_scores()
        
    def load_scores(self) -> List[Dict[str, any]]:
        if not os.path.exists(self.scores_file):
            return []
        try:
            with open(self.scores_file, 'r') as f:
                return json.loads(f.read())
        except:
            return []
        
    def save_score(self, name: str, score: int):
        scores = self.load_scores()
        scores.append({"name": name, "score": score})
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:10]
        
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f)
            
    def get_top_scores(self, limit: int = 5) -> List[Dict[str, any]]:
        return self.high_scores[:limit]
            
    def reload_scores(self):
        self.high_scores = self.load_scores()