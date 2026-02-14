/// <reference path="../_shared/edge-runtime.d.ts" />

Deno.serve(async (req: Request) => {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Max-Age': '86400',
  };

  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL');
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');

    if (!supabaseUrl || !supabaseKey) {
      throw new Error('Missing required environment variables: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');
    }

    const headers = {
      'apikey': supabaseKey,
      'Authorization': `Bearer ${supabaseKey}`,
    };

    const fetchJson = async (url: string) => {
      const response = await fetch(url, { headers });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Supabase REST request failed (${response.status}): ${text}`);
      }
      return response.json();
    };

    // Fetch all RPEs, axioms, and relationships
    const [rpes, axioms, relationships] = await Promise.all([
      fetchJson(`${supabaseUrl}/rest/v1/rpes?select=*&order=transcendence_score.desc`),
      fetchJson(`${supabaseUrl}/rest/v1/axioms?select=*&order=axiom_number.asc`),
      fetchJson(`${supabaseUrl}/rest/v1/knowledge_graph?select=*`),
    ]);

    // Build nodes array (RPEs + Axioms)
    const nodes = [
      ...rpes.map((rpe: any) => ({
        id: rpe.entity_id,
        entity_id: rpe.entity_id,
        name: rpe.name,
        une_signature: rpe.une_signature,
        transcendence_score: rpe.transcendence_score ?? 5,
        void_resonance: rpe.void_resonance ?? 5,
        type: 'rpe',
        heretical_intensity: rpe.heretical_intensity,
        paradox_engine: rpe.paradox_engine,
      })),
      ...axioms.map((axiom: any) => ({
        id: axiom.entity_id ?? `AXM-${axiom.axiom_number}`,
        entity_id: axiom.entity_id ?? `AXM-${axiom.axiom_number}`,
        name: axiom.title,
        une_signature: 'Axiom',
        transcendence_score: 10,
        void_resonance: 10,
        type: 'axiom',
        axiom_number: axiom.axiom_number,
      })),
    ];

    const nodeIds = new Set(nodes.map((node: any) => node.id));

    // Build links array from relationships and keep only resolvable edges
    const links = relationships
      .map((rel: any) => ({
      source: rel.source_entity_id,
      target: rel.target_entity_id,
      type: rel.relationship_type,
      strength: rel.relationship_strength ?? 1,
      description: rel.description,
      }))
      .filter((rel: any) => nodeIds.has(rel.source) && nodeIds.has(rel.target));

    return new Response(
      JSON.stringify({ 
        data: { nodes, links },
        count: { nodes: nodes.length, links: links.length }
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return new Response(
      JSON.stringify({ error: { code: 'FUNCTION_ERROR', message: errorMessage } }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});
