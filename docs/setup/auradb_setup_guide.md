# Neo4j AuraDB Cloud Setup Guide

**Date:** October 28, 2025  
**Purpose:** Cloud Neo4j instance for portable development  
**Timeline:** 10 minutes

---

## Step 1: Sign Up for AuraDB Free Tier

1. **Go to:** https://neo4j.com/cloud/aura/
2. **Click:** "Start Free" or "Try Free"
3. **Sign up with:**
   - Email (use your academic email if available)
   - Create password
   - Verify email

---

## Step 2: Create Free Instance

1. **After login, click:** "Create Instance"
2. **Select:** "AuraDB Free"
3. **Configure:**
   - **Instance name:** `kikuyu-proverbs-dev`
   - **Region:** Choose closest to you (e.g., us-east-1, europe-west1)
   - **Database version:** Latest (5.x)
4. **Click:** "Create"

---

## Step 3: Save Credentials (IMPORTANT!)

**⚠️ CRITICAL:** AuraDB will show credentials ONLY ONCE after creation!

You'll see:
```
Instance Created!
Connection URI: neo4j+s://xxxxx.databases.neo4j.io
Username: neo4j
Password: [randomly generated - SAVE THIS!]
```

**IMMEDIATELY SAVE THESE THREE ITEMS:**
1. **Connection URI** (starts with `neo4j+s://`)
2. **Username** (usually `neo4j`)
3. **Password** (random string - can't recover if lost!)

---

## Step 4: Update .env File

Once you have the credentials, I'll help you update the `.env` file with:

```env
# Neo4j AuraDB Cloud Configuration
NEO4J_AURADB_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_AURADB_USER=neo4j
NEO4J_AURADB_PASSWORD=your-generated-password

# Keep local config for future Docker use
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=ograg2025
NEO4J_DATABASE=neo4j  # AuraDB free tier uses 'neo4j' database

# Active configuration (switch between local/cloud)
NEO4J_ACTIVE=auradb  # or 'local' when using Docker
```

---

## Step 5: Test Connection

After updating `.env`, we'll test with:

```bash
python3 scripts/validate_neo4j_connection.py --cloud
```

---

## Step 6: Access Neo4j Browser (Optional)

AuraDB provides a web interface:
1. Go to: https://console.neo4j.io
2. Click on your instance: `kikuyu-proverbs-dev`
3. Click "Open with" → "Neo4j Browser"
4. Explore your graph visually

---

## Benefits of Cloud Setup

✅ **Portable:** Access from anywhere  
✅ **No local install:** Works immediately  
✅ **Free tier:** 200k nodes, 400k relationships (plenty for our 100 proverbs)  
✅ **Backup:** Automatic cloud backups  
✅ **Secure:** TLS encryption built-in  

---

## Limitations of Free Tier

- Storage: 50MB (sufficient for our ontology)
- No APOC plugins (we can work around this)
- Public internet access required
- Instance pauses after 3 days inactivity (restarts instantly)

---

## Next Steps After Setup

1. ✅ Test connection
2. ✅ Deploy enhanced schema
3. ✅ Load 100 proverbs
4. ✅ Create concept nodes
5. ✅ Build relationships

**Estimated time:** 1 hour after connection verified

---

*Document created for Day 1 Phase 1 setup*
