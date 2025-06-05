if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <port> <name> <image>"
  exit 1
fi

docker run -p $1:8080 --name $2 $3