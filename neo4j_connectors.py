from neo4j import GraphDatabase
from datetime import datetime
import os

class GraphDB:
    def __init__(self):
        uri = os.environ.get("NEO4J_URI")
        user = os.environ.get("NEO4J_USER")
        password = os.environ.get("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # ------------------ USER PROFILE ------------------
    def create_or_update_user(self, user_id, education, status, interested_role):
        with self.driver.session() as session:
            session.run("""
                MERGE (u:User {user_id: $user_id})
                SET u.education = $education,
                    u.status = $status,
                    u.interested_role = $interested_role
            """, user_id=user_id, education=education, status=status, interested_role=interested_role)

    # ------------------ SKILLS ------------------
    def add_skill(self, user_id, skill, confidence):
        with self.driver.session() as session:
            session.run("""
                MERGE (u:User {user_id: $user_id})
                MERGE (s:Skill {name: $skill})
                MERGE (u)-[r:HAS_SKILL]->(s)
                SET r.confidence = $confidence
            """, user_id=user_id, skill=skill, confidence=confidence)

    # ------------------ INTERACTION LOGGING ------------------
    def log_interaction(self, user_id, type_, details=None, skill=None, role=None):
        timestamp = datetime.utcnow().isoformat()
        with self.driver.session() as session:
        # Create interaction node
            session.run("""
                MERGE (u:User {user_id: $user_id})
                CREATE (i:Interaction {
                timestamp: $timestamp,
                type: $type,
                details: $details
            })
                MERGE (u)-[:PERFORMED]->(i)
        """, user_id=user_id, timestamp=timestamp, type=type_, details=details)

        # Link skill
            if skill:
                session.run("""
                MERGE (s:Skill {name: $skill})
                WITH s
                MATCH (i:Interaction {timestamp: $timestamp})
                MERGE (i)-[:RELATED_TO_SKILL]->(s)
            """, skill=skill, timestamp=timestamp)

        # Link role
            if role:
                session.run("""
                MERGE (r:Role {name: $role})
                WITH r
                MATCH (i:Interaction {timestamp: $timestamp})
                MERGE (i)-[:RELATED_TO_ROLE]->(r)
            """, role=role, timestamp=timestamp)


    # ------------------ RECOMMENDATIONS ------------------
    def get_recommendations(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:HAS_SKILL]->(s:Skill)
        WITH u, COLLECT(s.name) AS userSkills, u.interested_role AS role
        MATCH (other:User)-[:HAS_SKILL]->(os:Skill)
        WHERE other.user_id <> $user_id AND other.interested_role = role
        WITH u, userSkills, other, COLLECT(os.name) AS otherSkills
        WITH userSkills, otherSkills, other, apoc.coll.subtract(otherSkills, userSkills) AS missing
        UNWIND missing AS skill
        RETURN DISTINCT skill LIMIT 10
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            return [record["skill"] for record in result]

    def get_user_skills(self, user_id):
      query = """
      MATCH (u:User {user_id: $user_id})-[r:HAS_SKILL]->(s:Skill)
      RETURN s.name AS skill, r.confidence AS confidence
      """
      with self.driver.session() as session:
        result = session.run(query, user_id=user_id)
        return [(record["skill"], record["confidence"]) for record in result]


