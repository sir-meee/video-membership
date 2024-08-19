# Video membership project

User

## Content via Vimeo

Video
    -vimeo_id
    
Content
    -content: video
    -data:
        video: { vimeo_video_id: id_value }
    -Pricing (ManyToMany)

## Subscription via Stripe

Pricing
    -name
    -currency
    -id
    -price per month

Merchant / Subscription
    - User (foreign key)
    - stripe_subscription_id
    -status (active / cancelled / past_due / trial)
    - pricing (foreign key)