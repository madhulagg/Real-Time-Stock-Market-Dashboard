#!/usr/bin/env python3
"""
Test script for the Stock Market Dashboard
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulate import simulate, get_individual_stock_performance, SENSEX_30
import json

def test_portfolio_simulation():
    """Test portfolio simulation functionality"""
    print("🧪 Testing Portfolio Simulation...")
    
    try:
        # Test basic simulation
        result = simulate(period="1mo")
        print(f"✅ Portfolio simulation successful")
        print(f"   Initial: ₹{result['initial']:,}")
        print(f"   Final: ₹{result['final']:,}")
        print(f"   Return: ₹{result['return']:,} ({result['return_pct']:.2f}%)")
        return True
    except Exception as e:
        print(f"❌ Portfolio simulation failed: {e}")
        return False

def test_individual_stock():
    """Test individual stock analysis"""
    print("\n🧪 Testing Individual Stock Analysis...")
    
    try:
        # Test with a popular stock
        stock_data = get_individual_stock_performance("RELIANCE.NS", period="1mo")
        if stock_data:
            print(f"✅ Individual stock analysis successful")
            print(f"   Stock: {stock_data['symbol']}")
            print(f"   Initial Price: ₹{stock_data['initial_price']}")
            print(f"   Final Price: ₹{stock_data['final_price']}")
            print(f"   Return: {stock_data['total_return_pct']:.2f}%")
            print(f"   Signals: SMA={stock_data['signals']['sma']}, MOM={stock_data['signals']['momentum']}, RSI={stock_data['signals']['rsi']}")
            return True
        else:
            print("❌ Individual stock analysis returned no data")
            return False
    except Exception as e:
        print(f"❌ Individual stock analysis failed: {e}")
        return False

def test_sensex_stocks():
    """Test Sensex 30 stocks list"""
    print("\n🧪 Testing Sensex 30 Stocks List...")
    
    try:
        print(f"✅ Found {len(SENSEX_30)} stocks in Sensex 30")
        print(f"   First 5: {SENSEX_30[:5]}")
        print(f"   Last 5: {SENSEX_30[-5:]}")
        return True
    except Exception as e:
        print(f"❌ Sensex stocks test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Stock Market Dashboard - Test Suite")
    print("=" * 50)
    
    tests = [
        test_sensex_stocks,
        test_portfolio_simulation,
        test_individual_stock
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard is ready to use.")
        print("\nTo start the dashboard:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 