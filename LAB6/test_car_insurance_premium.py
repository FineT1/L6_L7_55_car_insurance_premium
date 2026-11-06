import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout

# =====================================================================
# Tests for annual_premium(car_type, driver_age, claims_last_3_years, has_anti_theft)
# =====================================================================

def test_annual_premium_unknown_car_type():
    """Branch: car_type not in BASE_PREMIUM (True)"""
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)

def test_annual_premium_underage_driver():
    """Branch: driver_age < 18 (True)"""
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)

def test_annual_premium_young_driver_no_claims_anti_theft():
    """
    Branches tested:
    - driver_age < 25 (True): +4000
    - claims_last_3_years == 0 (True): 20% discount (// 5)
    - has_anti_theft (True): -500
    Calculation: Hatchback base 8000 + 4000 = 12000; 12000 - 2400 = 9600; 9600 - 500 = 9100
    """
    assert annual_premium("hatchback", 20, 0, True) == 9100

def test_annual_premium_senior_driver_high_claims():
    """
    Branches tested:
    - driver_age >= 60 (True): +2000
    - claims_last_3_years > 2 (True): premium * 2
    - has_anti_theft (False): no discount
    Calculation: SUV base 15000 + 2000 = 17000; 17000 * 2 = 34000
    """
    assert annual_premium("suv", 65, 3, False) == 34000

def test_annual_premium_standard_driver_moderate_claims():
    """
    Branches tested:
    - driver_age between 25 and 59 (False for both age branches)
    - claims_last_3_years == 1 (False for 0 claims, False for > 2 claims)
    - has_anti_theft (False)
    Calculation: Sedan base 12000
    """
    assert annual_premium("sedan", 30, 1, False) == 12000


# =====================================================================
# Tests for no_claim_bonus(claim_free_years)
# =====================================================================

def test_no_claim_bonus_negative_years():
    """Branch: claim_free_years < 0 (True)"""
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)

def test_no_claim_bonus_zero_years():
    """Branch: claim_free_years < 1 (False for all >= branch conditions)"""
    assert no_claim_bonus(0) == 0

def test_no_claim_bonus_tier_1_to_2_years():
    """Branch: claim_free_years >= 1 (True)"""
    assert no_claim_bonus(2) == 20

def test_no_claim_bonus_tier_3_to_4_years():
    """Branch: claim_free_years >= 3 (True)"""
    assert no_claim_bonus(4) == 35

def test_no_claim_bonus_tier_5_plus_years():
    """Branch: claim_free_years >= 5 (True)"""
    assert no_claim_bonus(5) == 50


# =====================================================================
# Tests for claim_payout(damage_cost, insured_value, deductible, is_total_loss)
# =====================================================================

def test_claim_payout_negative_damage_cost():
    """Branch: damage_cost < 0 (True)"""
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-100, 50000, 5000, False)

def test_claim_payout_negative_deductible():
    """Branch: deductible < 0 (True, when damage_cost >= 0)"""
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(10000, 50000, -500, False)

def test_claim_payout_total_loss():
    """Branch: is_total_loss (True)"""
    assert claim_payout(20000, 50000, 5000, True) == 50000

def test_claim_payout_damage_less_than_deductible():
    """Branch: damage_cost <= deductible (True)"""
    assert claim_payout(3000, 50000, 5000, False) == 0

def test_claim_payout_exceeds_insured_value():
    """
    Branch: payout > insured_value (True)
    Calculation: 70000 - 5000 = 65000 > 50000 -> returns 50000
    """
    assert claim_payout(70000, 50000, 5000, False) == 50000

def test_claim_payout_standard():
    """
    Branch: payout > insured_value (False)
    Calculation: 15000 - 5000 = 10000 <= 50000 -> returns 10000
    """
    assert claim_payout(15000, 50000, 5000, False) == 10000