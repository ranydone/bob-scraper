"""
FULLY AUTOMATED BOB E-AUCTION SCRAPER
Uses Playwright for reliable JavaScript execution
Runs completely hands-free
"""

import asyncio
import json
import pandas as pd
from datetime import datetime
from collections import Counter
import sys

print("="*80)
print("🏦 AUTOMATED BOB E-AUCTION SCRAPER")
print("="*80)
print("\nInstalling dependencies...\n")

# Install Playwright
import subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "playwright"], check=True)
subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)

print("✅ Dependencies installed!\n")

from playwright.async_api import async_playwright

class AutomatedBOBScraper:
    """
    Fully automated scraper - no manual intervention needed
    """
    
    def __init__(self):
        self.url = 'https://bankofbaroda.bank.in/e-auction/e-auction-notices'
        self.properties = []
        
    async def scrape(self):
        """Main scraping method"""
        
        print(f"🌐 Opening: {self.url}\n")
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            # Create context with realistic user agent
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            try:
                # Navigate to page
                print("⏳ Loading page...")
                await page.goto(self.url, wait_until='networkidle', timeout=60000)
                
                # Wait for content to load
                print("⏳ Waiting for properties to load...")
                await asyncio.sleep(12)  # Wait for JavaScript
                
                # Scroll to trigger lazy loading
                print("📜 Scrolling page...")
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(3)
                
                print("✅ Page loaded!\n")
                
                # Extract properties using JavaScript
                print("🔍 Extracting properties...\n")
                
                properties_data = await page.evaluate('''() => {
                    const allProperties = [];
                    const selectors = ['[class*="property"]', '[class*="auction"]', '[class*="card"]', '[class*="item"]'];
                    
                    let allElements = [];
                    selectors.forEach(sel => {
                        const elements = document.querySelectorAll(sel);
                        allElements = [...allElements, ...Array.from(elements)];
                    });
                    
                    // Remove duplicates
                    allElements = Array.from(new Set(allElements));
                    
                    allElements.forEach((elem, index) => {
                        const textContent = elem.innerText || '';
                        
                        if (textContent.length > 50 && /202[3-9]/.test(textContent)) {
                            const lines = textContent.split('\\n').filter(l => l.trim());
                            
                            // Extract property name (first line)
                            const propertyName = lines[0] || '';
                            
                            // Extract auction date
                            let auctionDate = '';
                            for (let i = 0; i < lines.length; i++) {
                                if (lines[i] === 'Auction Date' && i + 1 < lines.length) {
                                    auctionDate = lines[i + 1];
                                    break;
                                }
                            }
                            
                            // Extract zone
                            let zone = '';
                            for (let i = 0; i < lines.length; i++) {
                                if (lines[i] === 'Zone' && i + 1 < lines.length) {
                                    zone = lines[i + 1];
                                    break;
                                }
                            }
                            
                            // Extract region
                            let region = '';
                            for (let i = 0; i < lines.length; i++) {
                                if (lines[i] === 'Region' && i + 1 < lines.length) {
                                    const nextLine = lines[i + 1];
                                    if (nextLine !== 'Know More') {
                                        region = nextLine;
                                    }
                                    break;
                                }
                            }
                            
                            if (auctionDate) {
                                allProperties.push({
                                    property_name: propertyName,
                                    auction_date: auctionDate,
                                    zone: zone,
                                    region: region,
                                    full_text: textContent.substring(0, 500)
                                });
                            }
                        }
                    });
                    
                    return allProperties;
                }''')
                
                # Process and deduplicate
                seen = set()
                for prop in properties_data:
                    key = (prop['property_name'], prop['auction_date'])
                    if key not in seen:
                        seen.add(key)
                        
                        # Extract branch from property name
                        property_name = prop['property_name']
                        branch = ''
                        
                        if 'Branch:' in property_name:
                            parts = property_name.split('Branch:')
                            property_name = parts[0].strip().rstrip(',')
                            branch = parts[1].strip() if len(parts) > 1 else ''
                        
                        self.properties.append({
                            'id': len(self.properties) + 1,
                            'borrower_name': property_name,
                            'branch': branch,
                            'auction_date': prop['auction_date'],
                            'zone': prop['zone'],
                            'region': prop['region'],
                            'source': 'Bank of Baroda E-Auction',
                            'url': self.url,
                            'scraped_at': datetime.now().isoformat()
                        })
                
                print(f"✅ Extracted {len(self.properties)} unique properties\n")
                
            except Exception as e:
                print(f"❌ Error during scraping: {e}")
                
            finally:
                await browser.close()
    
    def display_results(self):
        """Display extracted properties"""
        if not self.properties:
            print("⚠️ No properties found")
            return
        
        print("="*80)
        print("📋 ALL PROPERTIES")
        print("="*80)
        
        for prop in self.properties:
            print(f"\n{prop['id']}. {prop['borrower_name'][:70]}")
            print(f"   📅 Auction: {prop['auction_date']}")
            if prop['branch']:
                print(f"   🏢 Branch: {prop['branch'][:50]}")
            print(f"   📍 Zone: {prop['zone']}")
            if prop['region']:
                print(f"   🗺️  Region: {prop['region']}")
    
    def show_statistics(self):
        """Show summary statistics"""
        if not self.properties:
            return
        
        print(f"\n{'='*80}")
        print("📊 STATISTICS")
        print(f"{'='*80}\n")
        
        print(f"Total Properties: {len(self.properties)}")
        
        # By date
        dates = Counter([p['auction_date'] for p in self.properties])
        print(f"\n📅 By Auction Date:")
        for date in sorted(dates.keys()):
            print(f"  {date}: {dates[date]} properties")
        
        # By zone
        zones = Counter([p['zone'] for p in self.properties if p['zone']])
        print(f"\n📍 By Zone:")
        for zone in sorted(zones.keys()):
            print(f"  {zone}: {zones[zone]} properties")
    
    def save_results(self):
        """Save to multiple formats"""
        if not self.properties:
            print("⚠️ No properties to save")
            return
        
        print(f"\n{'='*80}")
        print("💾 SAVING FILES")
        print(f"{'='*80}\n")
        
        # Save JSON
        with open('bob_automated_scrape.json', 'w') as f:
            json.dump(self.properties, f, indent=2)
        print("✅ JSON: bob_automated_scrape.json")
        
        # Save CSV
        df = pd.DataFrame(self.properties)
        df.to_csv('bob_automated_scrape.csv', index=False)
        print("✅ CSV: bob_automated_scrape.csv")
        
        # Save Excel
        with pd.ExcelWriter('bob_automated_scrape.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Automated Scrape')
            
            # Auto-adjust columns
            worksheet = writer.sheets['Automated Scrape']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col))
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
        
        print("✅ Excel: bob_automated_scrape.xlsx")
        
        # Save summary
        summary = {
            'scraped_at': datetime.now().isoformat(),
            'source_url': self.url,
            'total_properties': len(self.properties),
            'properties': self.properties
        }
        
        with open('bob_scrape_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        print("✅ Summary: bob_scrape_summary.json")
    
    async def run(self):
        """Run complete scraping process"""
        await self.scrape()
        self.display_results()
        self.show_statistics()
        self.save_results()

# Main execution
async def main():
    scraper = AutomatedBOBScraper()
    await scraper.run()
    
    print(f"\n{'='*80}")
    print("✅ AUTOMATED SCRAPING COMPLETE!")
    print(f"{'='*80}\n")
    print("📁 All files saved in current directory")
    print("🎉 Ready to use!")

if __name__ == "__main__":
    asyncio.run(main())
