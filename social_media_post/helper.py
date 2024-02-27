import requests

def create_linkedin_post(page_id,access_token,content):
    api_url  = 'https://api.linkedin.com/rest/posts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202402'  # Include the LinkedIn-Version header
    }
    data = {
    "author": f"urn:li:organization:{page_id}",
    "commentary": f"{content}",
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
    }

    response = requests.post(api_url, headers=headers, json=data)
    return response.status_code


def create_media_linkedin_post(page_id,access_token,content,media_url):
    api_url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202402'  # Include the LinkedIn-Version header
    }

    post_body = {
        'author': f'urn:li:organization:{page_id}',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': f'{content}',
                },
                'shareMediaCategory': 'ARTICLE',
                'media': [
                    {
                        'status': 'READY',
                        'description': {
                            'text': 'Read our latest blog post about LinkedIn API!',
                        },
                        'originalUrl': f'{media_url}',
                        "thumbnails": [
                            {
                                "url": f'{media_url}'
                            }
                        ],
                    },
                ],
            },
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
        },


    }

    response = requests.post(api_url, headers=headers, json=post_body)
    return response.status_code

