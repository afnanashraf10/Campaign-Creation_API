from django.shortcuts import render, redirect
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebookads.adobjects.ad import Ad
from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.targeting import Targeting
from facebook_business.api import FacebookAdsApi
from django.conf import settings

access_token = settings.ACCESS_TOKEN
app_id = settings.APP_ID
app_secret = settings.APP_SECRET
user_id = settings.USER_ID

def home(request):
	FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

	my_account = AdAccount('act_' + user_id)

	campaign = Campaign(parent_id=my_account.get_id_assured())

	context = {
		"id": campaign.get_id()

	}
	return render(request, 'fbapp/home.html', context)

def view_campaign(request):
	FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

	my_account = AdAccount('act_' + user_id)

	campaigns = my_account.get_campaigns()
	result = []
	for i in range(len(campaigns)):
		campaign = {}
		campaign['name'] = 'campaign-'+str(i+1)
		campaign['id'] = campaigns[i]["id"]

		result.append(campaign)

	context = {
		'campaigns': result
	}

	return render(request, 'fbapp/view_campaign.html', context)

def view_adset(request):
	FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

	my_account = AdAccount('act_' + user_id)

	adsets = my_account.get_ad_sets()
	adset_id = []
	for i in range(len(adsets)):
		adset_id.append(adsets[i]["id"])

	adset_data = []
	for id in adset_id:
		adset = AdSet(fbid=id)
		fields = [
			AdSet.Field.name,
			AdSet.Field.effective_status,
			AdSet.Field.campaign_id,
			]
		adset.remote_read(fields=fields)

		result = {}
		result["id"] = id
		result["name"] = adset[AdSet.Field.name]
		result["campid"] = adset[AdSet.Field.campaign_id]
		adset_data.append(result)

	context = {
		'adsets': adset_data
	}

	return render(request, 'fbapp/view_adset.html', context)

def delete_campaign(request, camid):
	FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

	campaign = Campaign(camid)
	campaign.remote_delete()

	return redirect('view-campaign')

def delete_adset(request, adid):
	FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

	adset = AdSet(adid)
	adset.remote_delete()

	return redirect('view-adset')

def create_campaign(request):
	FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

	my_account = AdAccount('act_'+user_id)

	campaign = Campaign(parent_id=my_account.get_id_assured())
	campaign[Campaign.Field.name] = "first campaign"
	campaign[Campaign.Field.objective] = 'LINK_CLICKS'
	campaign[Campaign.Field.status] = 'PAUSED'

	campaign.remote_create()

	result = {
		"id": campaign.get_id()
	}

	return redirect('view-campaign')

def create_adset(request, camid):
	FacebookAdsApi.init(access_token=access_token, app_id=app_id, app_secret=app_secret)

	my_account = AdAccount('act_'+user_id)

	adset = AdSet(parent_id=my_account.get_id_assured())
	adset[AdSet.Field.name] = 'Mobile App Installs Ad Set 2'
	adset[AdSet.Field.promoted_object] = {
    	'application_id': app_id,
	}
	adset[AdSet.Field.campaign_id] = camid
	adset[AdSet.Field.daily_budget] = 10000
	adset[AdSet.Field.billing_event] = AdSet.BillingEvent.impressions
	adset[AdSet.Field.bid_amount] = 2
	adset[AdSet.Field.status] = 'PAUSED'
	adset[AdSet.Field.targeting] = {
		Targeting.Field.geo_locations: {
			'countries': ['US'],
		},
		Targeting.Field.publisher_platforms: ['facebook', 'audience_network'],
		Targeting.Field.device_platforms: ['mobile'],
		Targeting.Field.user_os: [
			'IOS',
		],
	}

	adset.remote_create()

	result = {
		"id": adset.get_id()
	}

	return redirect('view-adset')

