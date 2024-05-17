import pytest
from fastapi import status

from core.config import app_settings

URL_PREFIX = '/api/v1/links/'
MOCK_IP_ADDR = '192.168.123.132'
IP_SUBNET = '192.168.123.0/24'
TEST_URL = 'https://www.ya.ru/'
NUMBER_LINKS = 3
NUMBER_ACCESS = 3
MISSING_ID = 'XXXXXXXX'


@pytest.mark.asyncio
async def test_blocking_access(mock_client, async_client, async_session):
    mock_client.host = MOCK_IP_ADDR

    app_settings.block_subnets.append(IP_SUBNET)
    response = await async_client.get(URL_PREFIX)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    app_settings.block_subnets.remove(IP_SUBNET)
    response = await async_client.get(URL_PREFIX)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_link(mock_client, async_client, async_session):
    mock_client.host = MOCK_IP_ADDR

    response = await async_client.get(URL_PREFIX)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = await async_client.post(
        URL_PREFIX, json={'original_url': TEST_URL}
    )
    assert response.status_code == status.HTTP_201_CREATED
    link = response.json()
    assert link['original_url'] == TEST_URL

    response = await async_client.get(URL_PREFIX)
    assert response.status_code == status.HTTP_200_OK
    link = response.json()[0]
    assert link['original_url'] == TEST_URL

    response = await async_client.get(f'{URL_PREFIX}{link["id"]}')
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    response = await async_client.get(f'{URL_PREFIX}{MISSING_ID}')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = await async_client.delete(f'{URL_PREFIX}{link["id"]}')
    assert response.status_code == status.HTTP_200_OK

    response = await async_client.get(f'{URL_PREFIX}{link["id"]}')
    assert response.status_code == status.HTTP_410_GONE

    response = await async_client.get(URL_PREFIX)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    response = await async_client.patch(link['id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_batch_links(mock_client, async_client, async_session):
    mock_client.host = MOCK_IP_ADDR
    json = [{'original_url': TEST_URL}] * NUMBER_LINKS
    response = await async_client.post(f'{URL_PREFIX}batch', json=json)
    assert response.status_code == status.HTTP_201_CREATED

    response = await async_client.get(URL_PREFIX)
    assert response.status_code == status.HTTP_200_OK
    links = response.json()
    assert len(links) == NUMBER_LINKS
    for i in range(NUMBER_LINKS):
        assert links[i]['original_url'] == TEST_URL


@pytest.mark.asyncio
async def test_link_status(mock_client, async_client, async_session):
    mock_client.host = MOCK_IP_ADDR

    response = await async_client.get(f'{URL_PREFIX}{MISSING_ID}/status')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = await async_client.post(
        URL_PREFIX, json={'original_url': TEST_URL}
    )
    assert response.status_code == status.HTTP_201_CREATED
    link = response.json()

    for _ in range(NUMBER_ACCESS):
        response = await async_client.get(f'{URL_PREFIX}{link["id"]}')
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

    response = await async_client.get(f'{URL_PREFIX}{link["id"]}/status')
    assert response.status_code == status.HTTP_200_OK
    link_access_count = response.json()
    assert link_access_count['usages_count'] == NUMBER_ACCESS

    response = await async_client.get(
        f'{URL_PREFIX}{link["id"]}/status', params={'full_info': True}
    )
    assert response.status_code == status.HTTP_200_OK
    link_access = response.json()
    for i in range(NUMBER_ACCESS):
        assert link_access[i]['link_id'] == link['id']
        assert link_access[i]['ip_address'] == MOCK_IP_ADDR
