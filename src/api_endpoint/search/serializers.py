from rest_framework import serializers

class RedditV1Serializer(serializers.Serializer) : 

    quote = serializers.CharField()
    subreddits = serializers.ListField(child=serializers.CharField(allow_blank=False, trim_whitespace=True),
                                        allow_empty=False)
    commentKeywords = serializers.ListField() 
    postKeywords = serializers.ListField() 
    before = serializers.DateField()
    after = serializers.DateField()


    def create(self, validated_data) : 
        return(validated_data)
