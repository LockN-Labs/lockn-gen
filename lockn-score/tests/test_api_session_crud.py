"""API unit tests for session CRUD operations."""

from __future__ import annotations

from src.modes.game import GameMode
from src.modes.rally import RallyMode
from src.modes.solo import SoloMode


class TestSessionCRUD:
    """Test session creation, retrieval, and deletion."""

    def test_create_solo_session(self, client) -> None:
        """Test creating a new solo session."""
        response = client.post("/api/session/solo", json={"target_rally_count": 120})
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "solo"
        assert data["state"]["settings"]["targetRallyCount"] == 120
        assert data["state"]["active"] is True
        assert data["state"]["streak"] == 0

    def test_create_rally_session(self, client) -> None:
        """Test creating a new rally session."""
        response = client.post("/api/session/rally", json={"target_rally_count": 88})
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "rally"
        assert data["state"]["settings"]["targetRallyCount"] == 88
        assert data["state"]["active"] is True

    def test_create_game_session(self, client) -> None:
        """Test creating a new game session."""
        response = client.post(
            "/api/session/game",
            json={"points_to_win": 21, "serve_interval": 5, "best_of_sets": 3}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "game"
        assert data["state"]["settings"]["pointsToWin"] == 21
        assert data["state"]["settings"]["serveInterval"] == 5
        assert data["state"]["settings"]["bestOfSets"] == 3

    def test_get_session_not_found(self, client) -> None:
        """Test getting a non-existent session."""
        response = client.get("/api/session/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    def test_delete_session(self, client) -> None:
        """Test deleting a session."""
        # Create session
        create_response = client.post("/api/session/solo")
        assert create_response.status_code == 200
        session_id = create_response.json()["session_id"]

        # Delete session
        delete_response = client.delete(f"/api/session/{session_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["status"] == "deleted"

        # Verify deletion
        get_response = client.get(f"/api/session/{session_id}")
        assert get_response.status_code == 404


class TestSessionHitMiss:
    """Test hit and miss operations in different modes."""

    def test_solo_hit(self, client) -> None:
        """Test hitting in solo mode."""
        create_response = client.post("/api/session/solo")
        session_id = create_response.json()["session_id"]

        hit_response = client.post(f"/api/session/{session_id}/hit")
        assert hit_response.status_code == 200
        data = hit_response.json()
        assert data["event_type"] == "hit"
        assert data["state"]["streak"] == 1

    def test_solo_miss(self, client) -> None:
        """Test missing in solo mode."""
        create_response = client.post("/api/session/solo")
        session_id = create_response.json()["session_id"]

        # First hit
        client.post(f"/api/session/{session_id}/hit")

        # Then miss
        miss_response = client.post(f"/api/session/{session_id}/miss")
        assert miss_response.status_code == 200
        data = miss_response.json()
        assert data["event_type"] == "miss"
        assert data["state"]["game_over"] is True

    def test_rally_hit(self, client) -> None:
        """Test hitting in rally mode."""
        create_response = client.post("/api/session/rally")
        session_id = create_response.json()["session_id"]

        hit_response = client.post(f"/api/session/{session_id}/hit")
        assert hit_response.status_code == 200
        data = hit_response.json()
        assert data["event_type"] == "hit"
        assert data["state"]["rallyCount"] == 1

    def test_rally_miss(self, client) -> None:
        """Test missing in rally mode."""
        create_response = client.post("/api/session/rally")
        session_id = create_response.json()["session_id"]

        # First hit
        client.post(f"/api/session/{session_id}/hit")

        # Then miss
        miss_response = client.post(f"/api/session/{session_id}/miss")
        assert miss_response.status_code == 200
        data = miss_response.json()
        assert data["event_type"] == "miss"
        assert data["state"]["lastMissedBy"] is not None

    def test_game_point(self, client) -> None:
        """Test scoring a point in game mode."""
        create_response = client.post("/api/session/game")
        session_id = create_response.json()["session_id"]

        point_response = client.post(f"/api/session/{session_id}/point", params={"player": 1})
        assert point_response.status_code == 200
        data = point_response.json()
        assert data["event_type"] == "point"
        assert data["state"]["player1"] == 1

    def test_game_miss(self, client) -> None:
        """Test missing in game mode."""
        create_response = client.post("/api/session/game")
        session_id = create_response.json()["session_id"]

        # First score a point
        client.post(f"/api/session/{session_id}/point", params={"player": 1})

        # Then miss
        miss_response = client.post(f"/api/session/{session_id}/miss")
        assert miss_response.status_code == 200
        data = miss_response.json()
        assert data["event_type"] == "miss"
        assert data["state"]["player1"] == 1  # Player 1 should get the point


class TestSessionValidation:
    """Test request validation in session endpoints."""

    def test_solo_rejects_game_fields(self, client) -> None:
        """Test that solo mode rejects game-specific fields."""
        response = client.post("/api/session/solo", json={"points_to_win": 11})
        assert response.status_code == 422  # Unprocessable Entity

    def test_rally_rejects_game_fields(self, client) -> None:
        """Test that rally mode rejects game-specific fields."""
        response = client.post("/api/session/rally", json={"serve_interval": 5})
        assert response.status_code == 422

    def test_game_rejects_unknown_fields(self, client) -> None:
        """Test that game mode rejects unknown fields."""
        response = client.post("/api/session/game", json={"unknown_field": "value"})
        assert response.status_code == 422

    def test_game_rejects_target_rally_count(self, client) -> None:
        """Test that game mode rejects target_rally_count."""
        response = client.post("/api/session/game", json={"target_rally_count": 100})
        assert response.status_code == 422

    def test_solo_accepts_valid_target_rally_count(self, client) -> None:
        """Test that solo mode accepts valid target_rally_count."""
        response = client.post("/api/session/solo", json={"target_rally_count": 50})
        assert response.status_code == 200
        data = response.json()
        assert data["state"]["settings"]["targetRallyCount"] == 50

    def test_game_accepts_valid_points_to_win(self, client) -> None:
        """Test that game mode accepts valid points_to_win."""
        response = client.post("/api/session/game", json={"points_to_win": 15})
        assert response.status_code == 200
        data = response.json()
        assert data["state"]["settings"]["pointsToWin"] == 15


class TestRallyEnd:
    """Test rally-end endpoint for game mode."""

    def test_rally_end_game_mode(self, client) -> None:
        """Test rally-end endpoint in game mode."""
        create_response = client.post("/api/session/game")
        session_id = create_response.json()["session_id"]

        # Score a point first
        client.post(f"/api/session/{session_id}/point", params={"player": 1})

        rally_end_response = client.post(
            f"/api/session/{session_id}/rally-end",
            params={"rally_length": 10}
        )
        assert rally_end_response.status_code == 200
        data = rally_end_response.json()
        assert data["event_type"] == "rally_end"
        assert data["state"]["lastRallyCount"] == 10

    def test_rally_end_rejects_non_game_modes(self, client) -> None:
        """Test that rally-end rejects non-game modes."""
        # Try with solo mode
        create_response = client.post("/api/session/solo")
        session_id = create_response.json()["session_id"]

        response = client.post(f"/api/session/{session_id}/rally-end", params={"rally_length": 10})
        assert response.status_code == 400
        assert "only for game mode" in response.json()["detail"]


class TestManualScoreOverride:
    """Test manual score override functionality."""

    def test_manual_score_override_game_mode(self, client) -> None:
        """Test manual score override in game mode."""
        create_response = client.post("/api/session/game")
        session_id = create_response.json()["session_id"]

        # Score a point normally first
        client.post(f"/api/session/{session_id}/point", params={"player": 1})

        # Override: give player 2 a point
        override_response = client.post(
            f"/api/session/{session_id}/point",
            params={"player": 2}
        )
        assert override_response.status_code == 200
        data = override_response.json()
        assert data["state"]["player2"] == 1

    def test_manual_score_override_rejects_non_game_modes(self, client) -> None:
        """Test that manual score override rejects non-game modes."""
        create_response = client.post("/api/session/solo")
        session_id = create_response.json()["session_id"]

        response = client.post(f"/api/session/{session_id}/point", params={"player": 1})
        assert response.status_code == 400