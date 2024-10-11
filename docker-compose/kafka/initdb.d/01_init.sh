BOOTSTRAP_SERVER="127.0.0.1:9092"

kafka_ensure_topic_exists() {
    local topic=""
    local partitions=1
    local replication_factor=1

    while [ $# -gt 0 ]; do
	case $1 in
	    --topic) topic=$2; shift;;
	    --partitions) partitions=$2; shift;;
	    --replication-factor) replication_factor=$2; shift;;
	esac
	shift
    done

    if [ -z $topic ]; then
	echo "The --topic option is required" >&2
	return 1
    fi

    if kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVER --list |grep -q ^$topic; then
	local cur_partitions=$( kafka-topics.sh \
	    --bootstrap-server $BOOTSTRAP_SERVER \
	    --describe \
	    --topic $topic |grep 'Partition: [0-9]' |wc -l )
	if [ $cur_partitions -eq $partitions ]; then
	    return 0;
	fi
	echo "Updating topic $topic"
	kafka-topics.sh \
	    --bootstrap-server $BOOTSTRAP_SERVER \
	    --alter \
	    --topic $topic \
	    --partitions $partitions
    else 
	echo "Creating topic $topic"
	kafka-topics.sh \
	    --bootstrap-server $BOOTSTRAP_SERVER \
	    --create \
	    --topic $topic \
	    --replication-factor $replication_factor \
	    --partitions $partitions
    fi
}

/opt/bitnami/scripts/kafka/run.sh &
kafka_pid=$!

echo "Waiting for Kafka starts up..."
while ! kafka-topics.sh \
    --bootstrap-server $BOOTSTRAP_SERVER \
    --list; do
    sleep 0.5;
done

kafka_ensure_topic_exists --topic locations	--partitions 4
kafka_ensure_topic_exists --topic users		--partitions 4
kafka_ensure_topic_exists --topic weather	--partitions 8

sleep 1
echo "Shutting down Kafka..."
kill $kafka_pid
sleep 5
echo "Done Kafka initialization script."
