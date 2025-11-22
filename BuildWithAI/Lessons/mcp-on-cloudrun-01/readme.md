







gcloud config set project [PROJECT_ID]
Example:

gcloud config set project lab-project-id-example
If you can't remember your project id:
You can list all your project ids with:

gcloud projects list | awk '/PROJECT_ID/{print $2}'


