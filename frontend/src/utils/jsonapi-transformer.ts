/**
 * JSON:API Transformer - Versión Simplificada
 *
 * Convierte respuestas JSON:API en objetos planos fáciles de usar.
 *
 * JSON:API estructura:    { type, id, attributes: {...}, links: {...} }
 * Resultado transformado: { id, type, ...attributes, _links: {...} }
 */

// ============================================================================
// Types - Solo lo esencial
// ============================================================================

/**
 * Link HATEOAS con método HTTP
 */
export type LinkObject = {
  href: string
  method: string
}

/**
 * Recurso JSON:API como llega del backend
 */
type JsonApiResource = {
  type: string
  id: string
  attributes: Record<string, any>
  links?: Record<string, LinkObject>
  relationships?: Record<string, any>
}

/**
 * Respuesta JSON:API con colección de recursos
 */
type JsonApiCollectionResponse = {
  data: JsonApiResource[]
  links?: Record<string, LinkObject>
  meta?: Record<string, any>
  jsonapi?: { version: string }
}

// ============================================================================
// Funciones principales - Simple y directo
// ============================================================================

/**
 * Simplifica nombres de links removiendo prefijos
 * "reservas.obtener" → "obtener"
 */
function simplifyLinkNames(links?: Record<string, LinkObject>): Record<string, LinkObject> {
  if (!links) return {}

  const simplified: Record<string, LinkObject> = {}
  for (const [key, value] of Object.entries(links)) {
    // Tomar solo la última parte después del punto
    const simpleName = key.split('.').pop() || key
    simplified[simpleName] = value
  }
  return simplified
}

/**
 * Convierte un recurso JSON:API a objeto plano
 *
 * @example
 * const recurso = { type: "reservas", id: "1", attributes: { fecha: "2026-02-15" } }
 * const plano = transformResource(recurso)
 * // { id: "1", type: "reservas", fecha: "2026-02-15", _links: {...} }
 */
export function transformResource<T = any>(resource: JsonApiResource) {
  return {
    id: resource.id,
    type: resource.type,
    ...resource.attributes,
    _links: simplifyLinkNames(resource.links),
  } as T & {
    id: string
    type: string
    _links: Record<string, LinkObject>
  }
}

/**
 * Convierte colección JSON:API a array de objetos planos
 *
 * @example
 * const respuesta = { data: [...recursos], links: {...} }
 * const { data, _links } = transformCollection(respuesta)
 */
export function transformCollection<T = any>(response: JsonApiCollectionResponse): {
  data: Array<T & { id: string; type: string; _links: Record<string, LinkObject> }>
  _links: Record<string, LinkObject>
  meta?: Record<string, any>
} {
  return {
    data: response.data.map(transformResource<T>),
    _links: simplifyLinkNames(response.links),
    meta: response.meta,
  }
}
