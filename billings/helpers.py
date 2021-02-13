# Helpers

def get_claim_category_name(slug):
    if slug == 'mileage':
        return 'Mileage'

    if slug == 'fi':
        return 'FI'

    if slug == 'public_transport':
        return 'Public Transport'

    if slug == 'accommodation':
        return 'Accommodation'

    if slug == 'others':
        return 'Others'