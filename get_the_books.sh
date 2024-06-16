# Establish the list of book ids and the url
ids=("932" "1063" "1064" "2147" "2148" "2149" "2150" "2151" "10031" "17192")
url="https://www.gutenberg.org/cache/epub"

# Loop through the ids and download each text
for id in "${ids[@]}"; do
	# -qN will disregard files that have already been downloaded and quiet the message
	wget -qN "${url}/${id}/pg${id}.txt"
	echo "pg${id}.txt is ready to use!"
done
