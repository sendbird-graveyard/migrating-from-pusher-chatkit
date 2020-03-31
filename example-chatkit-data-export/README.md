# SAMPLE CHATKIT EXPORT 2020/03/26
**Everything in this export, including schemas, is provisional and subject to change.**

**All data is for example purposes only**

# Chatkit Data Export

## What's in this export
### JSON Schema
We have provided JSON schema for each exported entity (https://json-schema.org/specification-links.html#draft-7):
 - `schema/user.json`
 - `schema/room.json`
 - `schema/message.json`

### Export data
Exported data is in newline-delimited JSON format (https://github.com/ndjson/ndjson-spec)
 - `export/users.ndjson`
 - `export/rooms.ndjson`
 - `export/messages.ndjson`

## FAQ
 - Q: How do I download attachments?
 - A: Attachment URLs provided in the messages export have been signed for 7 days. Please download all media in this time window and host elsewhere.
 - Q: How do I parse datetimes (such as `created_at` and `updated_at`)?
 - A: Datetimes are formatted according to https://tools.ietf.org/html/rfc3339
