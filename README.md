# Migrating to SendBird from Pusher Chatkit

With SendBird, we make it easy to quickly perform a bulk migration of your user, channel and message chat data from Pusher’s Chatkit. Pusher is retiring their Chatkit product on April 23, 2020, but the SendBird team is ready to help you to migrate quickly! Tell us more about your chat migration at support@sendbird.com

## Migration Steps

### 1. Export your data from Pusher

- Export your data from Pusher. This data should consist of users, channels and messages.
- [Sign up for SendBird](https://dashboard.sendbird.com/auth/signup) and create your SendBird applications.
  We recommend creating two applications: one test/development application and one production application. SendBird can perform a dry run of your migration data into your test/development application prior to migration into your production application so you can verify the data import. When choosing a server region for your applications, select the region that is the closest to your end-users.
- Share your data import with SendBird. To get started, contact us at support@sendbird.com

### 2. Convert Pusher to SendBird

You can refer to [Pusher data format](https://github.com/sendbird/migrating-from-pusher-chatkit/example-chatkit-data-export) and [SendBird data format](https://github.com/sendbird/example-sendbird-data-json) then convert Pusher to SendBird. After converting it, you can contact us at support@sendbird.com then we will give you SFTP account info, validate your data and migrate it for you.

We will soon upload the sample conversion script here for Pusher to SendBird.

#### User (users.json)

- Maximum of 10,000 users per file, up to 10 MB per file
- Required: Please confirm if you would like users to be issued an access_token or not with the SendBird team before your user migration
- User reference information  
  https://pusher.com/docs/chatkit/reference/latest#users (Pusher)  
  https://docs.sendbird.com/platform/user (SendBird)
- Conversion grid
  |PUSHER|SENDBIRD|note|
  |---|---|---|
  |id|user_id||
  |name|nickname||
  |avatar_url|profile_url||
  |-|profile_file|if you have avatar files, you can name it using UUID|
  |metadata|custom_data||

#### Message (messages.json)

- Maximum of 1,000 channels per file, up to 10 MB per file
- Can be used to populate channel information, even if the channel does not have any messages
- Message reference information  
  https://pusher.com/docs/chatkit/reference/latest#rooms  
  https://pusher.com/docs/chatkit/reference/latest#messages (Pusher)  
  https://docs.sendbird.com/platform/messages (SendBird)
- Conversion grid
  |PUSHER||SENDBIRD|note|
  |---|---|---|---|
  |rooms.json|id|channel_url||
  ||name|name||
  ||created_by_id|-||
  ||member_ids|members||
  ||push_notification_title_override|-||
  ||private|is_public||
  ||custom_data|data (or custom_type)||
  ||created_at|created_at||
  ||-|cover_url||
  |messages.json|id|dedup_id||
  ||sender_id|user_id||
  ||created_at (or updated_at)|ts||
  ||parts|-|'inline' type (only) = MESG type|
  ||||'inline, url, and attachment' type = FILE type|

### 2. Prepare your app with SendBird SDK

While your data is importing into SendBird, begin development of a new version of your application running with the SendBird SDK. Find our getting started guides and sample apps below.

**JavaScript**

- [Quick Start Guide](https://docs.sendbird.com/javascript)
- [Sample Apps for Web and React Native](https://github.com/sendbird/sendbird-javascript)
- [See the Sample Apps running in action here!](http://sample.sendbird.com)

**Android**

- [Quick Start Guide](https://docs.sendbird.com/android)
- [Sample App](https://github.com/sendbird/sendbird-android)

**iOS**

- [Quick Start Guide](https://docs.sendbird.com/ios)
- [Sample App](https://github.com/sendbird/SendBird-iOS)

### 3. Deploy app code with SendBird SDK

After your data import is complete, it’s time to release the new app with SendBird SDK. If possible, we recommend force-updating your users to the new app version to quickly move all users to chat running with SendBird.

If it is not possible to immediately force-update users in your application, we recommend [getting in touch with us](support@sendbird.com) if this is your must-have use case so we can discuss and provide assistance in moving forward.

## Data Mappings

### Users

Users can chat with each other by participating in open channels and joining group channels and are identified with their own user id. [Users in SendBird](https://docs.sendbird.com/platform/user) are similar to [Users in Chatkit](https://pusher.com/docs/chatkit/reference/latest#users).

- **User id**: A string with a length of 80 and can be the same as the user id that was used in Chatkit. This will be the unique id that can be used to identify the user and we don’t allow duplicate id in an app.
- **Metadata**: Map your Chatkit user custom_data to user metadata in SendBird. If you want to add custom information such as organization id for the B2B case, you can use this resource. You can filter users based on this value to limit their access to a certain group of users. Find more information on [user metadata here](https://docs.sendbird.com/platform/user_metadata).
- **Access Token/Session Token**: Users can still have access [tokens as in Chatkit](https://pusher.com/docs/chatkit/authentication), but these are not required by default in SendBird. For ease of migration, we recommend adjusting your access token policy after migration is complete. Access tokens or session tokens require your system to save this value for future login to SendBird for this user. [Learn more on access tokens and session tokens here](https://docs.sendbird.com/platform/user#3_create_a_user_4_access_token_vs_session_token).

### Messages

SendBird supports text and file messages for migration and maps them to SendBird MESG and FILE message types.
[Learn more about message types here](https://docs.sendbird.com/platform/messages). A SendBird message is not broken into multiple parts like a [message in Chatkit](https://pusher.com/docs/chatkit/reference/latest#messages), so we recommend that a message with link or attachment parts is mapped to SendBird's FILE message type.

- **Custom Type**: You can use this field to subclassify messages. This field can be used for querying messages.
- **Data**: Reserved for adding custom data information used for clients. The data field stores string type data and customers can use JSON or XML to serialize data into the string.
- **Dedup id**: A unique id from the legacy system. A duplicate check will be performed on this field so it prevents the same data from getting inserted.
- **Created at**: Instead of the timestamp set at the saving step, you should assign the original value from the legacy system.
- **File message**: The file message can include the data of the file to upload to the SendBird server in raw binary format or the URL to the file.

### Channels

For every [Room in Chatkit](https://pusher.com/docs/chatkit/reference/javascript#rooms), there's a SendBird channel available. SendBird supports [Group Channels](https://docs.sendbird.com/platform/group_channel#3_create_a_channel) designed for chats with user membership similar to Room Membership in Chatkit. Group Channels can include 1-1 chats or 1-N chats with multiple members, and Group Channels can be public or private.

SendBird also supports [Open Channels](https://docs.sendbird.com/platform/open_channel) intended for large, public chats that users participate in during their active chat session. [Learn more about channel types here](https://docs.sendbird.com/platform/channel_type#2_channel_types).
During migration, when the channel is not found, SendBird creates a channel first and then starts adding messages.

- **Channel URL**: If you pass "channel_url" as the legacy system's channel identifier, then you don't have to save mapping info between legacy channels and SendBird channels. The channel_url is a unique identifier in your app so a duplicate channel URL will not be allowed.
- **Data**: Reserved for adding custom data information used for clients. The data field stores string type data and customers can use JSON or XML to serialize data into the string. You can also add origin information to mark that it was migrated.
- **Custom Type**: This value helps subclassify channels. This field can be used for querying channels. Tip- If the organization that your apps support have a hierarchy, give the customer type as higher_organization_name_sub_organization_name ex. macy_sanfrancisco. You can query channels based on custom_type_equal or custom_type_starts_with operator.
