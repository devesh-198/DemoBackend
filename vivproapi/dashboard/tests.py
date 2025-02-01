from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import DanceProfile

class DanceProfileListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data before running the tests."""
        cls.client = APIClient()

        # Create some test DanceProfile records
        DanceProfile.objects.create(id="7svJ308NOS6EMHd7D1YZnw", title="Song A", danceability=80, energy=70, mode=1, acousticness=20, tempo=120, duration_ms=180000, num_sections=5, num_segments=10, rating=4)
        DanceProfile.objects.create(id="2ftBcyzDa2REbBy7pMfbTT", title="Song B", danceability=60, energy=50, mode=0, acousticness=40, tempo=110, duration_ms=200000, num_sections=6, num_segments=15, rating=3)

    def test_get_dance_profiles(self):
        """Test retrieving dance profiles via API."""
        response = self.client.get("/api/dance-profiles/")

        # Check if response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if response has the expected structure
        self.assertIn("head", response.data)
        self.assertIn("body", response.data)

        body = response.data["body"]
        self.assertIn("tableHeaders", body)
        self.assertIn("tableData", body)
        self.assertIn("scatteredChart", body)
        self.assertIn("histogramChart", body)
        self.assertIn("barchart", body)

    def test_pagination(self):
        """Test if pagination works correctly."""
        response = self.client.get("/api/dance-profiles/?pageNumber=0&perPageCount=1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["body"]["tableData"]), 1)

    def test_sorting(self):
        """Test sorting functionality."""
        response = self.client.get("/api/dance-profiles/?sortBy=danceability&order=ASC")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data["body"]["tableData"]
        self.assertGreaterEqual(data[1][2], data[0][2])  # Danceability should be sorted in ASC order

    def test_filtering(self):
        """Test filtering by song title."""
        response = self.client.get("/api/dance-profiles/?songTitle=Song A")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["body"]["tableData"]), 1)



class SetStarRatingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data before running the tests."""
        cls.client = APIClient()

        # Create a test song in DanceProfile
        cls.song = DanceProfile.objects.create(
            id="7svJ308NOS6EMHd7D1YZnw",
            title="Test Song",
            danceability=75,
            energy=60,
            mode=1,
            acousticness=30,
            tempo=130,
            duration_ms=210000,
            num_sections=4,
            num_segments=8,
            rating=3
        )

    def test_set_star_rating_success(self):
        """Test if the rating updates successfully."""
        payload = {"songId": self.song.id, "rating": 5}
        response = self.client.post("/api/dance-rating/", payload, format="json")

        # Check if response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the rating is updated in the database
        self.song.refresh_from_db()
        self.assertEqual(self.song.rating, 5)

