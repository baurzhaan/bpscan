from typing import Dict, List, Any

def compare_cis_to_browser(
    cis_policies: Dict[str, Any],
    browser_policies: List[Dict[str, str]],
) -> List[Dict[str, Any]]:

    results = []

    browser_lookup = {
        p["Policy name"].lower(): p.get("Policy value").strip()
        for p in browser_policies
    }

    for policy_id, cis_entry in cis_policies.items():
        if policy_id.lower() not in browser_lookup:
            continue
        
        cis_recommended_value = cis_entry.get("recommended_value")
        default_value = cis_entry.get("default_value") 
        browser_value = browser_lookup.get(policy_id.lower())

        if browser_value == "":
            effective_value = default_value
            source = "default"
        else:
            effective_value = browser_value
            source = "explicit"
        
        compliant = False
        if effective_value and effective_value in cis_recommended_value:
            compliant = True
        if not effective_value and not cis_recommended_value:
            compliant = True

        results.append({
            "policy_id": policy_id,
            "policy_name": cis_entry.get("policy_name"),
            "level": cis_entry.get("level"),
            "browser_value": browser_value,
            "effective_value": effective_value,
            "cis_recommended_value": cis_recommended_value,
            "compliant": compliant,
            "value_source": source,
            "CIS ID": cis_entry.get("cis_id"),
        })

    return results
