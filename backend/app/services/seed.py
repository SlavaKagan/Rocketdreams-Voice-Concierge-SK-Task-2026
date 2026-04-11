from sqlalchemy.orm import Session
from app.models.models import FAQItem, VoiceConfig
from app.core.database import SessionLocal
from app.services.embedding import get_embedding

FAQ_DATA = [
    # General
    {"category": "General", "question": "What are the casino hours?", "answer": "The casino is open 24 hours a day, 7 days a week."},
    {"category": "General", "question": "What time is check-in and check-out?", "answer": "Check-in is at 4:00 PM (early check-in subject to availability). Check-out is at 11:00 AM. Late checkout is available for suite guests."},
    {"category": "General", "question": "Is parking available?", "answer": "Valet parking is complimentary for hotel guests and $25 for visitors. Self parking is free for all guests."},
    {"category": "General", "question": "What is the dress code?", "answer": "Smart casual throughout the property. Formal attire is required at Aurelia restaurant and Eclipse Lounge after 8 PM."},
    {"category": "General", "question": "What is the age requirement?", "answer": "Guests must be 21 or older for the casino floor and bars. All ages are welcome in the hotel and family restaurants."},
    {"category": "General", "question": "Is Wi-Fi available?", "answer": "Complimentary Wi-Fi is available throughout the property. Premium high-speed Wi-Fi is available in suites."},

    # Gaming
    {"category": "Gaming", "question": "What slot machines are available?", "answer": "We have over 2,000 machines ranging from $0.01 to $1,000 per spin, including the latest video slots, classic reels, and progressive jackpots. The largest jackpot is currently at $4.2 million."},
    {"category": "Gaming", "question": "Tell me about blackjack tables.", "answer": "We have 40 blackjack tables with minimums from $25 to $10,000. Single deck, 6-deck, and Spanish 21 are available."},
    {"category": "Gaming", "question": "Is the poker room open?", "answer": "Yes, our poker room is open 24/7. We offer Texas Hold'em (No Limit and Limit), Omaha, and Seven Card Stud. Daily tournaments at 11 AM and 7 PM with a $200 buy-in."},
    {"category": "Gaming", "question": "What roulette options are available?", "answer": "We have 12 roulette tables including American, European, and French roulette. Minimums start from $15."},
    {"category": "Gaming", "question": "Tell me about baccarat.", "answer": "We have 8 baccarat tables in the main casino and a private high-limit salon with 4 tables. Minimums from $50, high-limit from $5,000."},
    {"category": "Gaming", "question": "Are there craps tables?", "answer": "Yes, we have 6 craps tables with minimums from $15. Free lessons are available daily at 10 AM."},
    {"category": "Gaming", "question": "Tell me about the sports book.", "answer": "Our sports book is an 80-seat theater with a 40-foot screen and full bar service. Mobile betting is available throughout the property via the Meridian app."},
    {"category": "Gaming", "question": "What is the high limit salon?", "answer": "The High Limit Salon is a private gaming area with dedicated hosts, available by invitation or with a $50,000 credit line. It includes private restrooms, complimentary dining, and personal butler service."},
    {"category": "Gaming", "question": "What is the Meridian Rewards program?", "answer": "The Meridian Rewards program lets you earn points on all play. Tiers include Gold, Platinum, Diamond, and the invite-only Black tier."},

    # Accommodations
    {"category": "Accommodations", "question": "What room types are available?", "answer": "We offer Deluxe Rooms from $299/night, Premier Rooms from $449/night, Luxury Suites from $799/night, Penthouse Suites from $2,500/night, and the Chairman's Villa by inquiry only."},
    {"category": "Accommodations", "question": "Tell me about the deluxe room.", "answer": "The Deluxe Room is 450 sq ft with a king or two queens, city or pool view. From $299 per night."},
    {"category": "Accommodations", "question": "Tell me about the penthouse suite.", "answer": "The Penthouse Suite is 1,800 sq ft with two bedrooms, a dining room, butler's pantry, and private terrace. From $2,500 per night."},
    {"category": "Accommodations", "question": "Do you have accessible rooms?", "answer": "Yes, accessible rooms are available in all categories with roll-in showers, lowered amenities, and visual alerts. Please request at booking."},

    # Restaurants
    {"category": "Dining", "question": "What restaurants are on property?", "answer": "We have Aurelia (fine dining, French), Silk Road (Pan-Asian), The Steakhouse (American), Café Meridian (casual all-day), and Pool Bar & Grill (poolside, seasonal)."},
    {"category": "Dining", "question": "Tell me about Aurelia restaurant.", "answer": "Aurelia is our signature fine dining restaurant featuring modern French cuisine by Chef Marcus Webb, who holds 2 Michelin stars. The tasting menu is $285 per person. Open for dinner only, 6 PM to 10 PM. Reservations required, formal attire."},
    {"category": "Dining", "question": "Tell me about Silk Road.", "answer": "Silk Road offers Pan-Asian cuisine with a sushi bar, robata grill, and dim sum. Open 11 AM to 11 PM daily. Reservations recommended for dinner. Smart casual, $40-80 per person."},
    {"category": "Dining", "question": "Tell me about The Steakhouse.", "answer": "The Steakhouse is a classic American steakhouse featuring dry-aged beef and fresh seafood. Open 5 PM to 11 PM. Reservations recommended. Smart casual, $70-150 per person."},
    {"category": "Dining", "question": "Is there casual dining available?", "answer": "Café Meridian offers casual all-day dining with a breakfast buffet 7-11 AM for $45, and lunch and dinner until midnight. No reservations needed."},

    # Bars & Lounges
    {"category": "Bars", "question": "Tell me about Eclipse Lounge.", "answer": "Eclipse Lounge is our rooftop bar with stunning Strip views, craft cocktails, and a champagne menu. Open 5 PM to 2 AM. Formal attire required after 8 PM."},
    {"category": "Bars", "question": "Is there a whiskey bar?", "answer": "The Vault is our whiskey and cigar lounge with over 400 whiskey selections and a humidor with premium cigars. Open 4 PM to 2 AM. 21+ only."},
    {"category": "Bars", "question": "Are drinks complimentary at the casino?", "answer": "Yes, complimentary drinks are available for active players at our 6 casino floor bars."},

    # Entertainment
    {"category": "Entertainment", "question": "Tell me about the spa.", "answer": "Meridian Spa is a full-service spa and salon offering massage, facials, and body treatments. Couples suites are available. Open 8 AM to 8 PM. Booking 24 hours in advance is recommended."},
    {"category": "Entertainment", "question": "Is there a fitness center?", "answer": "Yes, our fitness center is open 24 hours for hotel guests and includes Peloton bikes, free weights, a yoga studio, and personal training services."},
    {"category": "Entertainment", "question": "Tell me about the pool.", "answer": "We have a pool complex with three pools including an adults-only infinity pool. Cabanas are available from $300 per day, including a $100 food credit. Open 8 AM to 8 PM."},
    {"category": "Entertainment", "question": "What entertainment is available at the theater?", "answer": "The Meridian Theater is a 1,200-seat venue with internationally acclaimed artist residencies. Tickets start from $95 with VIP packages available. Check the website for the current schedule."},
    {"category": "Entertainment", "question": "Is there a nightclub?", "answer": "NOVA is our premier nightclub, open Friday and Saturday from 10:30 PM to 4 AM. General cover is $50, tables start from $2,000. Hotel guests can access the guest list."},

    # Special Events
    {"category": "Events", "question": "Do you host weddings?", "answer": "Yes, we offer multiple wedding venues from an intimate chapel to a grand ballroom. Packages range from $5,000 to $150,000, with a wedding coordinator included in all packages."},
    {"category": "Events", "question": "Can I host a private event?", "answer": "Yes, we have meeting rooms and ballrooms from 500 to 15,000 sq ft with full catering and AV services. Corporate rates are available."},
    {"category": "Events", "question": "Do you offer birthday or anniversary packages?", "answer": "Yes, celebration packages start at $500 additional and include a room upgrade, champagne, custom cake, and dinner credit. 72-hour advance notice required."},
    {"category": "Events", "question": "Do you have bachelor or bachelorette packages?", "answer": "Yes, VIP packages start at $3,000 and include a suite, nightclub table, pool cabana, and spa credits. Must book at least 1 week in advance."},

    # Partner Discounts
    {"category": "Partners", "question": "Are there any nearby restaurant discounts?", "answer": "Yes! Show your room key at Carbone, an excellent Italian fine dining restaurant 5 minutes away, for 15% off food and priority reservations."},
    {"category": "Partners", "question": "Are there any partner discounts?", "answer": "Yes, with your room key you get: 15% off at Carbone, $10 off Omega Mart, 20% off helicopter Strip tours at Vegas Nights Aviation, a free hour at Top Golf with 2-hour booking, 10% off Spa Aquae at JW Marriott, and a VIP SlotZilla pass at Fremont Street Experience."},
    {"category": "Partners", "question": "Is there a helicopter tour discount?", "answer": "Yes, Vegas Nights Aviation offers Meridian guests 20% off Strip tours and complimentary champagne. Just show your room key."},
]

def seed():
    db: Session = SessionLocal()
    try:
        existing = db.query(FAQItem).count()
        if existing > 0:
            print(f"Database already seeded with {existing} FAQ items. Skipping.")
            return

        print(f"Seeding {len(FAQ_DATA)} FAQ items...")
        for i, item in enumerate(FAQ_DATA):
            print(f"  [{i+1}/{len(FAQ_DATA)}] Embedding: {item['question']}")
            embedding = get_embedding(item["question"] + " " + item["answer"])
            faq = FAQItem(
                question=item["question"],
                answer=item["answer"],
                category=item["category"],
                embedding=embedding
            )
            db.add(faq)

       # Seed default voice config
        from app.core.constants import DEFAULT_VOICE_ID
        voice_config = VoiceConfig(active_voice_id=DEFAULT_VOICE_ID)
        db.add(voice_config)

        db.commit()
        print("✅ Seeding complete!")
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()