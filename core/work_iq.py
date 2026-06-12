import hashlib


class WorkIQSimulator:
    """Simulated Work IQ Organizational Context Generator for nodes."""
    
    DEVELOPERS = ["Sarah Chen", "Marcus Vance", "Elena Rostova", "Alex Mercer"]
    MESSAGES = [
        "Hey team, this module has been failing on prod occasionally. I think there is a concurrency leak in the connection pool.",
        "Refactoring this class today to fit the new Auth spec. Ping me if you hit any import breaks.",
        "Let's add test coverage for this function before the sprint review. Fabric IQ shows it has 0% coverage currently.",
        "OWASP scan flagged this section for weak hashing. We should migrate this to PBKDF2 as soon as possible.",
        "This is deprecated code from v1. Please don't write any new imports pointing to this module.",
        "We discussed this file in the standup meeting on June 8th. The plan is to split it into microservices next sprint."
    ]

    @classmethod
    def get_signals(cls, node_name, seed_str):
        """Generate work signals (commit context, teams context) for a node."""
        h = int(hashlib.md5(seed_str.encode()).hexdigest()[:4], 16)
        
        # Commit context
        author = cls.DEVELOPERS[h % len(cls.DEVELOPERS)]
        commits_count = 3 + (h % 20)
        days_ago = h % 30
        
        # Teams context
        msg_count = 1 + (h % 3)
        teams_msgs = []
        for i in range(msg_count):
            msg_idx = (h + i) % len(cls.MESSAGES)
            teams_msgs.append({
                "sender": cls.DEVELOPERS[(h + i + 1) % len(cls.DEVELOPERS)],
                "timestamp": f"{days_ago + i} days ago",
                "message": cls.MESSAGES[msg_idx]
            })

        return {
            "author": author,
            "commitsCount": commits_count,
            "lastModified": f"{days_ago} days ago",
            "teamsDiscussions": teams_msgs,
            "prComment": f"Resolved PR review comment: 'Refactor {node_name} to prevent cyclic dependencies.'"
        }
