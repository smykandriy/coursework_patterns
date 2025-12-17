import apiClient from '../api/client'
import { QuoteResponse } from '../types'

const pricingService = {
  async quote(carId: string, start: string, end: string): Promise<QuoteResponse> {
    const response = await apiClient.get('/pricing/quote/', {
      params: { car: carId, start, end }
    })
    return response.data as QuoteResponse
  }
}

export default pricingService
