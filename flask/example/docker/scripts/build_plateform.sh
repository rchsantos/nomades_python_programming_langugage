if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <image_name> <dockerfile_path>"
  exit 1
fi

docker build -t $1 --platform=linux/amd64 $2