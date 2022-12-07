from rest_framework import serializers

class RedditV1Serializer(serializers.Serializer) : 

    search_string = serializers.CharField()
    subreddits = serializers.CharField(allow_blank=False, trim_whitespace=True)
    filter_keywords = serializers.CharField() 
    description = serializers.CharField()



    def create(self, validated_data) : 
        return(validated_data)
