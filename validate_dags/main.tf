
resource "google_storage_bucket" "dags_bucket" {
  name = "dags-bkt-01"
  location  = "us-central1"

}

resource "google_storage_bucket" "tmp_dags_bucket" {
  name = "tmp-dags-bkt-01"
  location  = "us-central1"
}

resource "google_pubsub_topic" "notifications_topic" {
  name = "dags-notification-topic"
}

resource "google_pubsub_topic_iam_binding" "binding" {
  topic       = "${google_pubsub_topic.notifications_topic.name}"
  role        = "roles/pubsub.publisher"

  members     = ["serviceAccount:service-[PROJECT_ID]@gs-project-accounts.iam.gserviceaccount.com"]
}

resource "google_storage_notification" "notification" {
  bucket            = "${google_storage_bucket.tmp_dags_bucket.name}"
  payload_format    = "JSON_API_V1"
  topic             = "${google_pubsub_topic.notifications_topic.id}"
  event_types       = ["OBJECT_FINALIZE", "OBJECT_METADATA_UPDATE"]
  depends_on        = ["google_pubsub_topic_iam_binding.binding"]
}