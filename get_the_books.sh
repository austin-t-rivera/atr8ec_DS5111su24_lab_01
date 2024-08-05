# Establish the list of book ids and the url
ids=("932" "1063" "1064" "2147" "2148" "2149" "2150" "2151" "10031" "14082" "17192")
url="https://www.gutenberg.org/cache/epub"

# Create a "gutenbooks" directory if it does not exist
mkdir -p "gutenbooks"

# Loop through the ids and download each text
for id in "${ids[@]}"; do
	# Set output path
	output_path="gutenbooks/pg${id}.txt"

	# -qN will disregard files that have already been downloaded and quiet the message
	wget -qN "${url}/${id}/pg${id}.txt" -O "${output_path}"
	echo "pg${id}.txt is ready to use!"
done
